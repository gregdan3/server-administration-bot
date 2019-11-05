#!/usr/bin/env python3
import argparse
from functools import partial

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

__all__ = []

_log = logging.getLogger(__name__)


def init_logger(log_level, log_file, log_file_level):
    LOG_FORMAT = (
        "[%(asctime)s] [%(filename)22s:%(lineno)-4s] [%(levelname)8s]   %(message)s"
    )
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    if log_file:
        file_hander = logging.FileHandler(log_file)
        file_hander.setLevel(log_file_level)
        file_hander.setFormatter(logging.Formatter(LOG_FORMAT))
        logging.getLogger().addHandler(file_hander)


def bot_command(update, context, execute):
    stdout = execute()
    if not stdout:
        return
    message = "``` " + stdout + " ```"  # TODO
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def bot_send(bot, prefix, execute, suffix, sendto):
    stdout = execute()
    if not stdout:
        return
    message = prefix + "``` " + stdout + " ```" + suffix  # TODO
    bot.sendMessage(chat_id=sendto, text=message, parse_mode=ParseMode.MARKDOWN)


def prep_commands(bot, commands: list):
    for _, command in commands.items():
        reactto = command["reactto"]
        execute = command["execute"]
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
            bot_send(bot, prefix, partial(get_command_out, execute), suffix, sendto)

        else:  # constants to run regularly
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

    updater = Updater(token, use_context=True)  # handles Commands
    bot = Bot(token)  # handles Constants

    all_commands = load_yml_file(argv.config)

    constants = all_commands.get("constants", [])
    commands = all_commands.get("commands", [])

    if constants == []:
        _log.WARNING("No constants provided; none will be loaded!")
    if commands == []:
        _log.WARNING("No commands provided; none will be loaded!")

    prep_constants(bot, constants)
    prep_commands(updater, commands)

    updater.start_polling()
    updater.idle()


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
        type=str.upper,
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
