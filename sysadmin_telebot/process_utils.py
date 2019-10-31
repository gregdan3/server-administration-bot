#!/usr/bin/env python3
import multiprocessing
import subprocess
import time
import traceback


__all__ = ["get_command_out", "every"]


def call_command(*args, **kwargs):
    print(args, kwargs)
    return subprocess.call(*args)


def get_command_out(*args, **kwargs):
    stdout, stderr = execute_command(*args, **kwargs)
    return clean_output(stdout, stderr)


def execute_command(*args, **kwargs):
    proc = subprocess.Popen(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.communicate()


def clean_output(stdout, stderr, handler=None):
    if stderr:
        if handler is not None:
            pass  # TODO
        return None
    return stdout.decode("UTF-8")


def every(delay, task, *args, **kwargs):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task(*args, **kwargs)
        except Exception:
            traceback.print_exc()
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


def main():
    result = get_command_out("uname -r")
    print(result)


if __name__ == "__main__":
    main()
