import os
from typing import Optional
from signal import SIGTERM


def is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def terminate_process(pid: Optional[int]):
    if pid is not None:
        if is_pid_alive(pid):
            os.kill(pid, SIGTERM)
