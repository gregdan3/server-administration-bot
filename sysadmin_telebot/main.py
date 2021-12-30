#!/usr/bin/env -S python3 -OO
import argparse
from functools import partial
import logging
import sys

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
from sysadmin_telebot.file_utils import TG_BOT_KEY, load_yml_file
from sysadmin_telebot.log_utils import init_logger
from sysadmin_telebot.arguments import BaseArgParser

__all__ = []

_log = logging.getLogger(__name__)


def format_backticks(s):
    return "``` " + str(s) + " ```"  # TODO: gross formatting


def bot_command(update, context, execute):
    stdout = execute()
    if not stdout:
        update.message.reply_text("No command output.")
        return
    message = format_backticks(stdout)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def bot_send(bot, prefix, execute, suffix, sendto):
    stdout = execute()
    if not stdout:
        return
    message = prefix + format_backticks(stdout) + suffix
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

    _log.info("Creating help command.")

    def help_command(update, context):
        update.message.reply_text(
            format_backticks(
                {
                    command["reactto"]: command["execute"]
                    for _, command in commands.items()
                }
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    bot.dispatcher.add_handler(CommandHandler("help", help_command))

    _log.info("Creating out-command for unknown command usages")

    def unknown_command(update, context):
        update.message.reply_text("Sorry, I didn't understand that command.")

    bot.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))


def prep_constants(bot, constants: list):
    for _, command in constants.items():
        seconds = command.get("every", "")
        prefix = command.get("prefix", "")
        execute = command["execute"]
        suffix = command.get("suffix", "")
        sendto = command["sendto"]

        if isinstance(sendto, list):
            for receiver in sendto:
                run_constant_in_thread(bot, seconds, prefix, execute, suffix, receiver)
        else:
            run_constant_in_thread(bot, seconds, prefix, execute, suffix, sendto)


def run_constant_in_thread(bot, seconds, prefix, execute, suffix, sendto):
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

    bot = Bot(TG_BOT_KEY)  # handles Constants
    updater = Updater(TG_BOT_KEY, use_context=True)  # handles Commands

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
