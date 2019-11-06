#!/usr/bin/env -S python3 -OO
import logging
import subprocess
import time
import threading
import traceback


__all__ = ["get_command_out", "every", "repeat_in_thread"]

_log = logging.getLogger(__name__)


def execute_command(*args, **kwargs):
    proc = subprocess.Popen(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.communicate()


def clean_output(stdout, stderr, handler=None):
    if stderr:
        if handler is not None:
            stderr = handler(stderr.decode("UTF-8"))
            return (stdout, stderr)
        _log.error("Handler not provided; stderr: %s", stderr.decode("UTF-8"))
        return None
    return stdout.decode("UTF-8")


def get_command_out(*args, **kwargs):
    stdout, stderr = execute_command(*args, **kwargs)
    return clean_output(stdout, stderr, **kwargs)


def every(delay, *args, **kwargs):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            for arg in args:
                arg(**kwargs)
        except Exception:
            traceback.print_exc()
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


def repeat_in_thread(seconds, *args, **kwargs):
    threading.Thread(target=lambda: every(seconds, *args, **kwargs)).start()


def main():
    result = get_command_out("uname -r")
    print(result)


if __name__ == "__main__":
    main()
