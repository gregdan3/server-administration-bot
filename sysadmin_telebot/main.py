#!/usr/bin/env python3
import argparse
from functools import partial

from telegram.bot import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    InlineQueryHandler,
)

from sysadmin_telebot.process_utils import get_command_out, every, repeat_in_thread
from sysadmin_telebot.file_utils import load_token, load_yml_file

__all__ = []


def hello(update, context):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def send(bot, message, chat_id):
    bot.sendMessage(chat_id=chat_id, text=message)


def send_command(bot, prefix, command_func, suffix, chat_id):
    out = command_func()
    message = prefix + out + suffix
    send(bot, message, chat_id)


def prep_constants(bot, constants: list):
    for _, command in constants.items():
        seconds = command.get("every", "")
        prefix = command.get("prefix", "")
        execute = command["execute"]
        suffix = command.get("suffix", "")
        sendto = command["sendto"]

        if seconds == "":  # init constants to run immediately
            stdout = get_command_out(execute)
            bot_send(bot, prefix + stdout + suffix, sendto)

        else:  # constants to run regularly
            repeat_in_thread(
                seconds,
                partial(
                    send_execution,
                    bot,
                    prefix,
                    partial(get_command_out, execute),
                    suffix,
                    sendto,
                ),
            )


def main(argv):
    """ dispatcher can handle Prompts based on Context, i.e., commands beginning with / in a chat 
        bot can handle sending any message at any given time, and this can be threaded! """
    token = load_token(argv.token)
    updater = Updater(token, use_context=True)
    bot = Bot(token)

    commands = load_yml_file(argv.config)

    init = commands.pop("init", None)
    if init is not None and isinstance(init, dict):
        init_wrapper(bot, init)

    for key, command in commands.items():
        command_wrapper(bot, command)

    updater.dispatcher.add_handler(CommandHandler("hello", hello))

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
