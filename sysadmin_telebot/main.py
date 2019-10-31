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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default="token.txt",
        help="The name of the file containing your bot's token.",
    )

    argv = parser.parse_args()
