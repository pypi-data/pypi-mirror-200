import asyncio
import copy
import logging
import traceback
from asyncio import StreamReader, FIRST_EXCEPTION
from datetime import datetime, timezone, timedelta
from subprocess import PIPE, STDOUT, Popen
from typing import List, Tuple, Optional, Dict, TypeAlias, Callable, Any, Union

from dateutil.parser import parse as dateutil_parse


def dump_rfc3339(dt: datetime, *, no_milliseconds=True) -> str:
    assert dt.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    if no_milliseconds:
        dt = dt.replace(microsecond=0)  # not interested in sub second precision
    res = dt.isoformat()
    if res.endswith("+00:00"):
        # +00:00 is nicer to write as Z (Zulu timezone)
        # But both are valid.
        res = res[:-6] + "Z"
    return res


def parse_rfc3339(date_str: str) -> datetime:
    # dateutil_parse parses ISO 8601, which contains almost all of RFC3339. This is good enough.
    res = dateutil_parse(date_str)
    assert res.tzinfo is not None  # assert timezone aware (non-naive) datetime
    return res


def _helper_convert_dict_datetimes_to_rfc3339(
    a_dict_or_list: Union[Dict, List], *, no_milliseconds=True
) -> List[Union[Dict, List]]:
    res = []
    if isinstance(a_dict_or_list, Dict):
        for key, value in a_dict_or_list.items():
            if isinstance(value, List) or isinstance(value, dict):
                res.append(value)
            if isinstance(value, datetime):
                a_dict_or_list[key] = dump_rfc3339(
                    value, no_milliseconds=no_milliseconds
                )
    elif isinstance(a_dict_or_list, List):
        for i in range(len(a_dict_or_list)):
            value = a_dict_or_list[i]
            if isinstance(value, List) or isinstance(value, dict):
                res.append(value)
            if isinstance(value, datetime):
                a_dict_or_list[i] = dump_rfc3339(value, no_milliseconds=no_milliseconds)
    return res


def convert_dict_datetimes_to_rfc3339(a_dict: Dict) -> Dict:
    """
    :param a_dict:
    :return: a deep copy of a_dict, but with each datetime anywhere, replaces by its representatino as a RFC3339 string
    """
    res = copy.deepcopy(a_dict)
    todo = [res]
    while todo:
        todo.extend(_helper_convert_dict_datetimes_to_rfc3339(todo.pop()))
    return res


def datetime_now(*, zulu=False, no_milliseconds=False) -> datetime:
    res = datetime.now(timezone.utc)
    if not zulu:
        res = res.astimezone(timezone(timedelta(hours=0), name="UTC"))
    if no_milliseconds:
        res = res.replace(microsecond=0)
    assert res.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    return res


def call_external_command_sync(*params: str, **kwargs) -> Tuple[int, str]:
    res = ""
    com: List[str] = list(params)
    kwargs["stdout"] = PIPE
    kwargs["stderr"] = STDOUT
    kwargs["universal_newlines"] = True
    with Popen(com, **kwargs) as proc:
        for line in proc.stdout:
            res += line
        res_code = proc.wait()
        # if res_code != 0:
        #     raise Exception('Command returned error ({}): {} (command={} )'.format(res_code, res.strip(), com))
        return res_code, res.strip()


OutputHandler: TypeAlias = Callable[[str], None]
NO_OUTPUT = lambda msg: None


async def log_output(out: OutputHandler, stream: StreamReader):
    saw_eof = False
    while not saw_eof:
        line = await stream.readline()
        if line:
            out(line.decode())
        else:
            saw_eof = True


async def call_external_command_async(
    *,
    command: List[str],
    cwd: Optional[str] = None,
    env: Dict[str, str] = {},
    timeout_s=3600,
    stdout_handler: OutputHandler = NO_OUTPUT,
    stderr_handler: OutputHandler = NO_OUTPUT,
    debug_log_handler: OutputHandler = NO_OUTPUT,
    error_log_handler: OutputHandler = NO_OUTPUT,
) -> int:
    assert command
    assert isinstance(command, list)
    assert all(isinstance(c, str) for c in command)

    env = dict(env)
    # await add_log(
    #     perftest_id,
    #     LogLevel.DEBUG,
    #     f"Will run command: {command!r} with env={env} in cwd={cwd}",
    #     session=session,
    # )
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,
    )
    tasks = []
    stdout_log_task = asyncio.create_task(log_output(stdout_handler, proc.stdout))
    stderr_log_task = asyncio.create_task(log_output(stderr_handler, proc.stderr))
    tasks.append(stdout_log_task)
    tasks.append(stderr_log_task)
    proc_done_task = asyncio.create_task(proc.wait())
    tasks.append(proc_done_task)

    pre_wait = datetime_now()

    debug_log_handler(
        f"Started command. Will wait for up to {timeout_s} seconds. Starting at {pre_wait}"
    )

    done, pending = await asyncio.wait(
        tasks,
        timeout=timeout_s,
        return_when=FIRST_EXCEPTION,
    )
    post_wait = datetime_now()
    logging.debug(
        f"(pre_wait={pre_wait} post_wait={post_wait}) len(done)={len(done)} len(pending)={len(pending)}"
    )
    if pending:
        saw_exception = False
        for d in done:
            e = d.exception()
            if e:
                saw_exception = True
                logging.error("Saw exception waiting", exc_info=e)
                tb = "".join(traceback.format_exception(None, e, e.__traceback__))
                error_log_handler(
                    f"Command exception: Will be cancelled. "
                    f"(pre_wait={pre_wait} post_wait={post_wait} e={e} {tb})",
                )
        if not saw_exception:
            error_log_handler(
                f"Command did not return within {timeout_s} seconds: Will be cancelled. "
                f"(pre_wait={pre_wait} post_wait={post_wait})",
            )
        for p in pending:
            p.cancel()
            proc.kill()
        raise TimeoutError("command timed out")
    else:
        debug_log_handler(
            f"Command exited with exitcode {proc.returncode}",
        )
        return proc.returncode


def is_naive_dt(v: datetime) -> bool:
    return v.tzinfo is None


def is_non_naive_dt(v: datetime) -> bool:
    return v.tzinfo is not None


def is_non_naive_opt_dt(v: Optional[datetime]) -> bool:
    return v is None or v.tzinfo is not None


def assert_non_naive_dt(v: datetime):
    assert v.tzinfo is not None, 'time is naive "{}"'.format(v)


def assert_non_naive_opt_dt(v: Optional[datetime]):
    assert v is None or v.tzinfo is not None, 'time is naive "{}"'.format(v)


def count_none(*args) -> int:
    """
    :return: the number of arguments that is None
    """
    res = 0
    for arg in args:
        res += int(arg is None)
    return res


def count_not_none(*args) -> int:
    """
    :return: the number of arguments that is not None
    """
    res = 0
    for arg in args:
        res += int(arg is not None)
    return res


def is_single_not_none(*args) -> bool:
    """
    :return: True if exactly one of the arguments is not None
    """
    res = 0
    for arg in args:
        res += int(arg is not None)
    return res == 1


def is_single_none(*args) -> bool:
    """
    :return: True if exactly one of the arguments is None
    """
    res = 0
    for arg in args:
        res += int(arg is None)
    return res == 1


def any_to_opt_bool(value: Any, default: Optional[bool] = None) -> Optional[bool]:
    if value is None:
        return default
    if value == 1:
        return True
    if value == 0:
        return False
    if str(value).lower() in ["true", "t", "1", "yes"]:
        return True
    if str(value).lower() in ["false", "f", "0", "no"]:
        return False
    return default


def any_to_bool(value: Any, default: Optional[bool] = None) -> bool:
    res = any_to_opt_bool(value, default)
    if res is not None:
        return res
    if default is None:
        raise ValueError('Could not convert "{}" to boolean value'.format(value))
    return default
