#!/usr/bin/env python3
import multiprocessing
import subprocess
import time
import traceback


def call_command(*args, **kwargs):
    print(args, kwargs)
    return subprocess.call(*args)


def execute_command(*args, **kwargs):
    proc = subprocess.Popen(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.communicate()
