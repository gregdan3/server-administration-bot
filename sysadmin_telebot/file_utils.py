#!/usr/bin/env python3
import os
import yaml
import __main__


__all__ = ["here", "load_token", "load_command"]

here = os.path.abspath(os.path.dirname(__main__.__file__))


def load_yml_file(filename):
    with open(filename, "r") as f:
        command = yaml.full_load(f)
    return command


def load_token(token_name):
    with open(os.path.join(here, token_name)) as f:
        token = f.readline().strip()
    return token


def main():
    print(load_yml_file(os.path.join(here, "local_config.yml")))


if __name__ == "__main__":
    main()
