import logging

__all__ = ["init_logger"]
_log = logging.getLogger(__name__)
LOG_FORMAT = (
    "[%(asctime)s] [%(filename)22s:%(lineno)-4s] [%(levelname)8s]   %(message)s"
)


def init_logger(log_level, log_file, log_file_level):
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    if log_file:
        file_hander = logging.FileHandler(log_file)
        file_hander.setLevel(log_file_level)
        file_hander.setFormatter(logging.Formatter(LOG_FORMAT))
        logging.getLogger().addHandler(file_hander)
