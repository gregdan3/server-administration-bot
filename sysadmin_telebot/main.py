#!/usr/bin/env python3
import logging
import sys
from functools import partial

from telegram.bot import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from sysadmin_telebot.arguments import BaseArgParser
from sysadmin_telebot.file_utils import TG_BOT_KEY, load_yml_file
from sysadmin_telebot.log_utils import init_logger
from sysadmin_telebot.process_utils import get_command_out
from sysadmin_telebot.telegram_utils import (
    bot_command,
    handle_message_queue,
    help_command,
    thread_command,
    unknown_command,
)
from sysadmin_telebot.thread_utils import create_message_thread, repeat_in_thread

__all__ = []
_log = logging.getLogger(__name__)


def prep_commands(bot, commands: dict):
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

    _log.info("Creating help command.")
    bot.dispatcher.add_handler(
        CommandHandler("help", partial(help_command, commands=commands))
    )

    _log.info("Creating out-command for unknown command usages")
    bot.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))


def prep_constants(constants: dict):
    for _, command in constants.items():
        seconds = command.get("every", 0)
        sleep = command.get("sleep", 0)
        prefix = command.get("prefix", "")
        execute = command["execute"]
        suffix = command.get("suffix", "")
        sendto = command["sendto"]

        if seconds == 0:  # init constants to run immediately
            _log.info("Executing %s, sending to %s", execute, sendto)
            thread_command(prefix, partial(get_command_out, execute), suffix, sendto)

        else:  # constants to run regularly
            _log.info("Executing %s every %s, sending to %s", execute, seconds, sendto)
            repeat_in_thread(
                seconds,
                partial(
                    thread_command,
                    prefix,
                    partial(get_command_out, execute),
                    suffix,
                    sendto,
                    sleep,
                ),
            )


def main(argv):
    init_logger(argv.log_level, argv.log_file, argv.log_file_level)

    bot = Bot(TG_BOT_KEY)  # handles Constants
    updater = Updater(TG_BOT_KEY, use_context=True)  # handles Commands

    create_message_thread(handle_message_queue, bot)
    # every message from a thread instead goes to a Queue
    # and a single thread reads from that queue

    all_commands = load_yml_file(argv.config)

    constants = all_commands.get("constants", {})
    commands = all_commands.get("commands", {})

    if not constants:
        _log.warning("No constants provided; none will be loaded!")
    if not commands:
        _log.warning("No commands provided; none will be loaded!")

    prep_constants(constants)
    prep_commands(updater, commands)

    try:
        _log.info("Bot is ready! Starting polling.")
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        _log.info("Shutting down updater thread.")
        updater.stop()


if __name__ == "__main__":
    parser = BaseArgParser()
    argv = parser.parse_args()
    if argv.danger_mode:
        _log.warning(
            "YOU ARE STARTING THE BOT IN DANGER MODE! Are you SURE you want to continue?"
        )
        _log.warning(
            "Users with access to the bot will be able to execute arbitrary commands on your system!"
        )
        if input("Y/N: ").lower() not in {"y", "yes"}:
            _log.warning("Prompt not accepted. Shutting down.")
            sys.exit()

    main(argv)
