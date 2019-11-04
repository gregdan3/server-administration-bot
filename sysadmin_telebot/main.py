#!/usr/bin/env python3
import argparse
import os
import threading

from telegram.bot import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    InlineQueryHandler,
)

from sysadmin_telebot.process_utils import get_command_out, every

__all__ = []


def load_token(token_name):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, token_name)) as f:
        token = f.readline().strip()
    return token


def hello(update, context):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def send(bot, message, chat_id):
    print(bot, message, chat_id)
    bot.sendMessage(chat_id=chat_id, text=message)


def main(argv):
    """ INTERNAL DOCS
        dispatcher can handle Prompts based on Context, i.e., commands beginning with / in a chat 
        bot can handle sending any message at any given time, and this can be threaded! """
    token = load_token(argv.token)
    updater = Updater(token, use_context=True)

    bot = Bot(token)

    updater.dispatcher.add_handler(CommandHandler("hello", hello))

    user = 1
    threading.Thread(
        target=lambda: every(
            3, send, bot=bot, message=get_command_out("uname -r"), chat_id=user
        )
    ).start()

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default="token.txt",
        help="The name of the file containing your bot's token.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="local_config.yml",
        help="The name of the file containing the commands you want your bot to execute.",
    )

    argv = parser.parse_args()
    main(argv)
