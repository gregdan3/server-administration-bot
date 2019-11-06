#!/usr/bin/env -S python3 -OO
import logging
import subprocess
import time
import threading
import traceback


__all__ = ["get_command_out", "every", "repeat_in_thread"]

_log = logging.getLogger(__name__)


def execute_command(*args, **kwargs):
    """ shell=True in subprocess.Popen is considered unsafe
        it is up to the user to provide sensible commands to execute.

        KNOWN PROBLEM: 
        A command which never outputs/sends an end of file
        will cause proc.communicate() to hang indefinitely. """
    proc = subprocess.Popen(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.communicate()


def clean_output(stdout, stderr, handler=None):
    """ no reason to do unnecessary decodes if we do not use the output 
        would be cleaner looking to do both decodes at top though

        handler should be a function that operates on stderr str """
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
    """ args is list of Callable
        kwargs is arguments to every Callable
        kwargs is redundant to use of functools.partial """
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            for arg in args:
                arg(**kwargs)
        except Exception:
            traceback.print_exc()
            # intentionally eat exception
            # bot will not fail, error does not propogate
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


def repeat_in_thread(seconds, *args, **kwargs):
    threading.Thread(target=lambda: every(seconds, *args, **kwargs)).start()


def main():
    result = get_command_out("uname -r")
    print(result)


if __name__ == "__main__":
    main()
