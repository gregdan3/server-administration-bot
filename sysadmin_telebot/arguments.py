import argparse


def BaseArgParser():
    """Provides an argparse.ArgumentParser with some arguments pre-prepared.
    The object is provided, as opposed to the already parsed args, so that
    another user/script may configure the parser even further if necessary."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="CONFIG_FILE",
        type=str,
        default="local_config.yml",
        help="Location of config file for all bot commands.",
    )
    parser.add_argument(
        "--danger-mode",
        dest="danger_mode",
        default=False,
        action="store_true",
        help="Enable Danger Mode: bot can execute arbitrary commands.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        metavar="LEVEL",
        type=str.upper,
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level to stdout.",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        metavar="LOG_FILE",
        type=str,
        default="",
        help="Log file to write to. No file logging by default.",
    )
    parser.add_argument(
        "--log-file-level",
        dest="log_file_level",
        metavar="LEVEL",
        type=str.upper,
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level to file.",
    )
    return parser  # allow user to configure later
