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


def hello(update, context):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def send(bot, message, chat_id):
    print(bot, message, chat_id)
    bot.sendMessage(chat_id=chat_id, text=message)
