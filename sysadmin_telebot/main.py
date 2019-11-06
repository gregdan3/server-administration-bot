#!/usr/bin/env -S python3 -OO
import argparse
from functools import partial
import logging

from telegram import ParseMode
from telegram.bot import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    InlineQueryHandler,
)

from sysadmin_telebot.process_utils import get_command_out, repeat_in_thread
from sysadmin_telebot.file_utils import load_token, load_yml_file
from sysadmin_telebot.log_utils import init_logger

__all__ = []

_log = logging.getLogger(__name__)


def bot_command(update, context, execute):
    stdout = execute()
    if not stdout:
        return
    message = "``` " + stdout + " ```"  # TODO: gross formatting
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def bot_send(bot, prefix, execute, suffix, sendto):
    stdout = execute()
    if not stdout:
        return
    message = prefix + "``` " + stdout + " ```" + suffix  # TODO: gross formatting
    bot.sendMessage(chat_id=sendto, text=message, parse_mode=ParseMode.MARKDOWN)


def prep_commands(bot, commands: list):
    for _, command in commands.items():
        reactto = command["reactto"]
        execute = command["execute"]
        _log.info("Adding command %s that executes %s", reactto, execute)
        # TODO: what if execute is very long
        bot.dispatcher.add_handler(
            CommandHandler(
                reactto, partial(bot_command, execute=partial(get_command_out, execute))
            )
        )


def prep_constants(bot, constants: list):
    for _, command in constants.items():
        seconds = command.get("every", "")
        prefix = command.get("prefix", "")
        execute = command["execute"]
        suffix = command.get("suffix", "")
        sendto = command["sendto"]

        if seconds == "":  # init constants to run immediately
            _log.info("Executing %s, sending to %s", execute, sendto)
            bot_send(bot, prefix, partial(get_command_out, execute), suffix, sendto)

        else:  # constants to run regularly
            _log.info("Executing %s every %s, sending to %s", execute, seconds, sendto)
            repeat_in_thread(
                seconds,
                partial(
                    bot_send,
                    bot,
                    prefix,
                    partial(get_command_out, execute),
                    suffix,
                    sendto,
                ),
            )


def main(argv):
    init_logger(argv.log_level, argv.log_file, argv.log_file_level)

    token = load_token(argv.token)

    bot = Bot(token)  # handles Constants
    updater = Updater(token, use_context=True)  # handles Commands

    all_commands = load_yml_file(argv.config)

    constants = all_commands.get("constants", [])
    commands = all_commands.get("commands", [])

    if constants == []:
        _log.warning("No constants provided; none will be loaded!")
    if commands == []:
        _log.warning("No commands provided; none will be loaded!")

    prep_constants(bot, constants)
    prep_commands(updater, commands)

    try:
        _log.info("Bot is ready! Starting polling.")
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        _log.info("Shutting down updater thread.")
        updater.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--token",
        dest="token",
        metavar="token",
        type=str,
        default="token.txt",
        help="The name of the file containing your bot's token.",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="config",
        type=str,
        default="local_config.yml",
        help="The name of the file containing the commands you want your bot to execute.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        metavar="log_level",
        type=str.upper,
        default="WARNING",
        help="Logging level to stdout",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        metavar="log_file",
        type=str,
        default="errors.log",
        help="Log file to write to",
    )
    parser.add_argument(
        "--log-file-level",
        dest="log_file_level",
        metavar="log_file_level",
        type=str.upper,
        default="WARNING",
        help="Logging level to file",
    )
    argv = parser.parse_args()
    main(argv)
