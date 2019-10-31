#!/usr/bin/env python3
import multiprocessing
import subprocess
import time
import traceback


__all__ = ["get_command_out"]


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


def main():
    result = get_command_out("uname -r")
    print(result)


if __name__ == "__main__":
    main()
