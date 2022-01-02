import logging
import subprocess

__all__ = ["get_command_out"]
_log = logging.getLogger(__name__)


def execute_command(*args, **kwargs):
    """shell=True in subprocess.Popen is considered unsafe
    it is up to the user to provide sensible commands to execute.

    KNOWN PROBLEM:
    A command which never outputs/sends an end of file
    will cause proc.communicate() to hang indefinitely."""
    _log.debug("From execute_command: %s", args)
    proc = subprocess.Popen(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.communicate()


def clean_output(stdout, stderr):
    """TODO: separate handling for stderr?"""
    return stdout.decode("UTF-8"), stderr.decode("UTF-8")


def get_command_out(*args, **kwargs):
    stdout, stderr = execute_command(*args, **kwargs)
    _log.debug("From get_command_out:\n\t%s\n\t%s", stdout, stderr)
    return clean_output(stdout, stderr)
