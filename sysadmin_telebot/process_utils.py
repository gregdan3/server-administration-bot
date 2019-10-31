#!/usr/bin/env python3
import multiprocessing
import subprocess
import time
import traceback


def call_command(*args, **kwargs):
    print(args, kwargs)
    return subprocess.call(*args)
