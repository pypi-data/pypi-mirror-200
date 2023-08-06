from typing import Any, Iterable, List, Mapping, Optional, Union
from typeguard import typechecked
from ..helper.accessories.color import (
    get_random_color, is_valid_color, colored
)
from ..helper.accessories.icon import get_random_icon
from ..helper.list.ensure_uniqueness import ensure_uniqueness
from ..helper.string.conversion import (
    to_cmd_name, to_variable_name, to_boolean
)
from ..helper.render_data import DEFAULT_RENDER_DATA
from ..helper.log import logger
from ..task_env.env import Env
from ..task_env.env_file import EnvFile
from ..task_group.group import Group
from ..task_input.base_input import BaseInput
from ..task_input._constant import RESERVED_INPUT_NAMES

import asyncio
import datetime
import os
import sys
import time
import jinja2


MAX_NAME_LENGTH = 20
MULTILINE_INDENT = ' ' * 8


class AnyExtensionFileSystemLoader(jinja2.FileSystemLoader):
    def get_source(self, environment, template):
        for search_dir in self.searchpath:
            file_path = os.path.join(search_dir, template)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    contents = file.read()
                    return contents, file_path, lambda: False
        raise jinja2.TemplateNotFound(template)


@typechecked
class TimeTracker():

    def __init__(self):
        self._start_time: float = 0
        self._end_time: float = 0

    def start_timer(self):
        self._start_time = time.time()

    def end_timer(self):
        self._end_time = time.time()

    def get_elapsed_time(self) -> float:
        return self._end_time - self._start_time


@typechecked
class AttemptTracker():

    def __init__(self, retry: int = 2):
        self.retry = retry
        self._attempt: int = 1

    def get_max_attempt(self) -> int:
        return self.retry + 1

    def get_attempt(self) -> int:
        return self._attempt

    def increase_attempt(self):
        self._attempt += 1

    def should_attempt(self) -> bool:
        attempt = self.get_attempt()
        max_attempt = self.get_max_attempt()
        return attempt <= max_attempt

    def is_last_attempt(self) -> bool:
        attempt = self.get_attempt()
        max_attempt = self.get_max_attempt()
        return attempt >= max_attempt


@typechecked
class FinishTracker():

    def __init__(self):
        self._execution_queue: Optional[asyncio.Queue] = None
        self._counter = 0

    async def mark_start(self):
        if self._execution_queue is None:
            self._execution_queue = asyncio.Queue()
        self._counter += 1

    async def mark_as_done(self):
        # Tracker might be started several times
        # However, when the execution is marked as done, it applied globally
        # Thus, we need to send event as much as the counter.
        for i in range(self._counter):
            await self._execution_queue.put(True)

    async def is_done(self) -> bool:
        while self._execution_queue is None:
            await asyncio.sleep(0.05)
        return await self._execution_queue.get()


@typechecked
class PidModel():

    def __init__(self):
        self.zrb_task_pid: int = os.getpid()

    def set_task_pid(self, pid: int):
        self.zrb_task_pid = pid

    def get_task_pid(self) -> int:
        return self.zrb_task_pid


@typechecked
class TaskDataModel():

    def __init__(
        self,
        name: str,
        group: Optional[Group] = None,
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: Optional[str] = None,
        color: Optional[str] = None,
    ):
        self.name = name
        self.group = group
        self.envs = [
            Env(name=key, os_name=key)
            for key in os.environ
        ] + envs
        self.env_files = env_files
        self.icon = icon
        self.color = color
        self._input_map: Mapping[str, Any] = {}
        self._env_map: Mapping[str, str] = {}
        self._complete_name: Optional[str] = None
        self._filled_complete_name: Optional[str] = None
        self._rendered_str: Mapping[str, str] = {}
        self._is_keyval_set = False  # Flag
        self._has_cli_interface = False
        self._render_data: Optional[Mapping[str, Any]] = None
        self._all_inputs: Optional[List[BaseInput]] = None

    def get_icon(self) -> str:
        if self.icon is None or self.icon == '':
            self.icon = get_random_icon()
        return self.icon

    def get_color(self) -> str:
        if self.color is None or not is_valid_color(self.color):
            self.color = get_random_color()
        return self.color

    def get_cmd_name(self) -> str:
        return to_cmd_name(self.name)

    def log_debug(self, message: Any):
        prefix = self._get_log_prefix()
        colored_message = colored(
            f'{prefix} • {message}', attrs=['dark']
        )
        logger.debug(colored_message)

    def log_warn(self, message: Any):
        prefix = self._get_log_prefix()
        colored_message = colored(
            f'{prefix} • {message}', attrs=['dark']
        )
        logger.warning(colored_message)

    def log_info(self, message: Any):
        prefix = self._get_log_prefix()
        colored_message = colored(
            f'{prefix} • {message}', attrs=['dark']
        )
        logger.info(colored_message)

    def log_error(self, message: Any):
        prefix = self._get_log_prefix()
        colored_message = colored(
            f'{prefix} • {message}', color='red', attrs=['bold']
        )
        logger.error(colored_message, exc_info=True)

    def log_critical(self, message: Any):
        prefix = self._get_log_prefix()
        colored_message = colored(
            f'{prefix} • {message}', color='red', attrs=['bold']
        )
        logger.critical(colored_message, exc_info=True)

    def print_out(self, msg: Any):
        prefix = self._get_colored_print_prefix()
        print(f'🤖 ➜  {prefix} • {msg}'.rstrip(), file=sys.stderr)

    def print_err(self, msg: Any):
        prefix = self._get_colored_print_prefix()
        print(f'🤖 ⚠  {prefix} • {msg}'.rstrip(), file=sys.stderr)

    def print_out_dark(self, msg: Any):
        self.print_out(colored(msg, attrs=['dark']))

    def colored(self, text: str) -> str:
        return colored(text, color=self.get_color())

    def play_bell(self):
        print('\a', end='', file=sys.stderr)

    def _get_colored_print_prefix(self) -> str:
        return self.colored(self._get_print_prefix())

    def _get_print_prefix(self) -> str:
        common_prefix = self._get_common_prefix(show_time=True)
        icon = self.get_icon()
        truncated_name = self._get_filled_complete_name()
        return f'{common_prefix} • {icon} {truncated_name}'

    def _get_log_prefix(self) -> str:
        common_prefix = self._get_common_prefix(show_time=False)
        icon = self.get_icon()
        filled_name = self._get_filled_complete_name()
        return f'{common_prefix} • {icon} {filled_name}'

    def _get_common_prefix(self, show_time: bool) -> str:
        attempt = self.get_attempt()
        max_attempt = self.get_max_attempt()
        pid = self.get_task_pid()
        if show_time:
            now = datetime.datetime.now().isoformat()
            return f'{now} ⚙ {pid} ➤ {attempt} of {max_attempt}'
        return f'⚙ {pid} ➤ {attempt} of {max_attempt}'

    def _get_filled_complete_name(self) -> str:
        if self._filled_complete_name is not None:
            return self._filled_complete_name
        complete_name = self._get_complete_name()
        self._filled_complete_name = complete_name.rjust(MAX_NAME_LENGTH, ' ')
        return self._filled_complete_name

    def get_input_map(self) -> Mapping[str, Any]:
        return self._input_map

    def get_env_map(self) -> Mapping[str, str]:
        return self._env_map

    def _inject_env_map(
        self, env_map: Mapping[str, str], override: bool = False
    ):
        for key, val in env_map.items():
            if override or key not in self._env_map:
                self._env_map[key] = val

    def render_any(self, val: Any) -> Any:
        if isinstance(val, str):
            return self.render_str(val)
        return val

    def render_float(self, val: Union[str, float]) -> float:
        if isinstance(val, str):
            return float(self.render_str(val))
        return val

    def render_int(self, val: Union[str, int]) -> int:
        if isinstance(val, str):
            return int(self.render_str(val))
        return val

    def render_bool(self, val: Union[str, bool]) -> bool:
        if isinstance(val, str):
            return to_boolean(self.render_str(val))
        return val

    def render_str(self, val: str) -> str:
        if val in self._rendered_str:
            return self._rendered_str[val]
        if not self._is_probably_jinja(val):
            return val
        template = jinja2.Template(val)
        data = self._get_render_data()
        self.log_debug(f'Render string template: {val}, with data: {data}')
        try:
            rendered_text = template.render(data)
            self.log_debug(f'Get rendered result: {rendered_text}')
        except Exception:
            self.log_error(f'Fail to render "{val}" with data: {data}')
        self._rendered_str[val] = rendered_text
        return rendered_text

    def render_file(self, location: str) -> str:
        location_dir = os.path.dirname(location)
        env = jinja2.Environment(
            loader=AnyExtensionFileSystemLoader([location_dir])
        )
        template = env.get_template(location)
        data = self._get_render_data()
        data['TEMPLATE_DIR'] = location_dir
        self.log_debug(f'Render template file: {template}, with data: {data}')
        rendered_text = template.render(data)
        self.log_debug(f'Get rendered result: {rendered_text}')
        return rendered_text

    def _get_render_data(self) -> Mapping[str, Any]:
        if self._render_data is not None:
            return self._render_data
        render_data = dict(DEFAULT_RENDER_DATA)
        render_data.update({
            'env': self._env_map,
            'input': self._input_map,
        })
        self._render_data = render_data
        return render_data

    def _get_multiline_repr(self, text: str) -> str:
        lines_repr: Iterable[str] = []
        lines = text.split('\n')
        if len(lines) == 1:
            return lines[0]
        for index, line in enumerate(lines):
            line_number_repr = str(index + 1).rjust(4, '0')
            lines_repr.append(f'{MULTILINE_INDENT}{line_number_repr} | {line}')
        return '\n' + '\n'.join(lines_repr)

    async def _set_local_keyval(
        self,
        kwargs: Mapping[str, Any],
        env_prefix: str = ''
    ):
        if self._is_keyval_set:
            return True
        self._is_keyval_set = True
        # Add self.inputs to input_map
        self.log_info('Set input map')
        for task_input in self.get_all_inputs():
            map_key = self._get_normalized_input_key(task_input.name)
            self._input_map[map_key] = self.render_any(
                kwargs.get(map_key, task_input.default)
            )
        self.log_debug(f'Input map: {self._input_map}')
        # Construct envs based on self.env_files and self.envs
        self.log_info('Merging env_files and envs')
        envs: Iterable[Env] = []
        for env_file in self.env_files:
            envs += env_file.get_envs()
        envs += self.envs
        envs.reverse()
        envs = ensure_uniqueness(
            envs, lambda x, y: x.name == y.name
        )
        envs.reverse()
        # Add envs to env_map
        self.log_info('Set env map')
        for task_env in envs:
            env_name = task_env.name
            if env_name in self._env_map:
                continue
            self._env_map[env_name] = self.render_any(
                task_env.get(env_prefix)
            )
        self.log_debug(f'Env map: {self._env_map}')

    def get_all_inputs(self) -> Iterable[BaseInput]:
        # Override this method!!!
        return self._all_inputs

    def _is_probably_jinja(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        if '{{' in value and '}}' in value:
            return True
        if '{%' in value and '%}' in value:
            return True
        return False

    def _get_normalized_input_key(self, key: str) -> str:
        if key in RESERVED_INPUT_NAMES:
            return key
        return to_variable_name(key)

    def _get_complete_name(self) -> str:
        if self._complete_name is not None:
            return self._complete_name
        executable_prefix = ''
        if self._has_cli_interface:
            executable_prefix += self._get_executable_name() + ' '
        cmd_name = self.get_cmd_name()
        if self.group is None:
            self._complete_name = f'{executable_prefix}{cmd_name}'
            return self._complete_name
        group_cmd_name = self.group.get_complete_name()
        self._complete_name = f'{executable_prefix}{group_cmd_name} {cmd_name}'
        return self._complete_name

    def _get_executable_name(self) -> str:
        if len(sys.argv) > 0 and sys.argv[0] != '':
            return os.path.basename(sys.argv[0])
        return 'zrb'

    def set_has_cli_interface(self):
        self._has_cli_interface = True


@typechecked
class TaskModel(
    TaskDataModel, PidModel, FinishTracker, AttemptTracker, TimeTracker
):

    def __init__(
        self,
        name: str,
        group: Optional[Group] = None,
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: Optional[str] = None,
        color: Optional[str] = None,
        retry: int = 2,
    ):
        TaskDataModel.__init__(
            self,
            name=name,
            group=group,
            envs=envs,
            env_files=env_files,
            icon=icon,
            color=color
        )
        retry = self.ensure_non_negative(retry, 'Find negative retry')
        PidModel.__init__(self)
        FinishTracker.__init__(self)
        AttemptTracker.__init__(self, retry=retry)
        TimeTracker.__init__(self)

    def ensure_non_negative(self, value: float, error_label: str) -> float:
        if value < 0:
            self.log_warn(f'{error_label}: {value}')
            return 0
        return value

    def show_done_info(self):
        complete_name = self._get_complete_name()
        elapsed_time = self.get_elapsed_time()
        message = '\n'.join([
            f'{complete_name} completed in {elapsed_time} seconds',
        ])
        self.print_out_dark(message)
        self.play_bell()
