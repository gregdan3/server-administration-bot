import logging
import queue
import time

import telegram
from telegram import ParseMode

_log = logging.getLogger(__name__)
MESSAGES = queue.Queue()


def format_backticks(s):
    return "```\n" + str(s) + "\n```"  # TODO: gross formatting


def help_command(update, context, commands={}):
    update.message.reply_text(
        format_backticks(
            {command["reactto"]: command["execute"] for _, command in commands.items()}
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


def unknown_command(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")


def bot_command(update, context, execute):
    """Used by telegram bot command registration"""
    stdout, stderr = execute()
    if not stdout:
        update.message.reply_text("No command output.")
        return
    message = format_backticks(stdout)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def thread_command(prefix, execute, suffix, sendto, sleep=0):
    """Used by a timed command thread to send messages to queue"""
    stdout, stderr = execute()
    if not stdout:
        return
    message = prefix + format_backticks(stdout) + suffix
    MESSAGES.put((sendto, message))
    if sleep > 0 and message:
        time.sleep(sleep)


def handle_message_queue(bot):
    """Consumes from message queue for sends"""
    _log.info("Consuming from message queue")
    while True:
        if MESSAGES.empty():
            time.sleep(1)
            continue
        try:
            chat_ids, msg = MESSAGES.get()
            for chat_id in chat_ids:
                bot.sendMessage(
                    chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN
                )
            MESSAGES.task_done()
        except telegram.error.RetryAfter:
            # TODO: time that Telegram tells us
            time.sleep(5)
        except telegram.error.TimedOut:
            time.sleep(5)
        # TODO: malformed command?
