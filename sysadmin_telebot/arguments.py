#!/usr/bin/env python3

import argparse


def BaseArgParser():
    """ Provides an argparse.ArgumentParser with some arguments pre-prepared.
        The object is provided, as opposed to the already parsed args, so that
        another user/script may configure the parser even further if necessary. """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--token",
        dest="token",
        metavar="TOKEN_FILE",
        type=str,
        default="token.txt",
        help="The name of the file containing your bot's token.",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="CONFIG_FILE",
        type=str,
        default="local_config.yml",
        help="The name of the file containing the commands you want your bot to execute.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        metavar="LEVEL",
        type=str.upper,
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level to stdout",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        metavar="LOG_FILE",
        type=str,
        default="errors.log",
        help="Log file to write to",
    )
    parser.add_argument(
        "--log-file-level",
        dest="log_file_level",
        metavar="LEVEL",
        type=str.upper,
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level to file",
    )
    return parser  # allow user to configure later


def main():
    parser = BaseArgParser()
    argv = parser.parse_args()
    print("argv.token:          %s" % argv.token)
    print("argv.config:         %s" % argv.config)
    print("argv.log_level:      %s" % argv.log_level)
    print("argv.log_file:       %s" % argv.log_file)
    print("argv.log_file_level: %s" % argv.log_file_level)


if __name__ == "__main__":
    main()
