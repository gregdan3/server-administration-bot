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
