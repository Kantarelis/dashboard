import os
import signal
import time
from typing import Optional


def is_pid_alive(pid: int) -> bool:
    """Function that check if a process of with the given pid is running."""
    try:
        os.kill(pid, 0)
        os.waitpid(pid, os.WNOHANG)
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def terminate_process(pid: Optional[int]) -> None:
    """Function - command that terminates a process with the given pid."""
    if pid is not None:
        if is_pid_alive(pid):
            print(f"REACHED: {pid}")
            os.kill(pid, signal.SIGTERM)
            # Wait to terminate
            time.sleep(1)
