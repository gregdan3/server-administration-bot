import logging
import threading
import time
import traceback
from functools import partial

__all__ = ["create_message_thread", "repeat_in_thread"]
_log = logging.getLogger(__name__)


def create_message_thread(message_handler, bot):
    _log.debug("Opening message thread with handler %s, bot %s", message_handler, bot)
    message_thread = threading.Thread(target=partial(message_handler, bot))
    message_thread.start()


def every(delay, *args, **kwargs):
    """args is list of Callable
    kwargs is arguments to every Callable
    kwargs is redundant to use of functools.partial"""
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
            # TODO: send errors to bot?
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


def repeat_in_thread(seconds, *args, **kwargs):
    threading.Thread(target=lambda: every(seconds, *args, **kwargs)).start()
