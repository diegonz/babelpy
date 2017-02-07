#!/usr/bin/env python3
import argparse
import os
import platform
import sys

from babelpy_utils.ConfigSettings import ConfigSettings

APP_ID = "babelPy"
APP_DESC = "An easy tool for those who would not survive in the tower of Babel"

arg_parser = argparse.ArgumentParser(description=APP_DESC, epilog="Enjoy!")
arg_parser.add_argument('-a', '--api-key', metavar='YourApiKey', nargs='?',
                        help='Your API key for target (or default) backend')
arg_parser.add_argument('-b', '--backend', metavar='yandex|other', nargs='?',
                        help='Target translate backend (Default: yandex)')
arg_parser.add_argument('-c', '--config-file', metavar='.babelPy.json',
                        nargs='?', help='Path to config file (load and save)')
arg_parser.add_argument('-s', '--source-lang', metavar='en|es', nargs='?',
                        help='Give a source language (avoids auto detection)')
arg_parser.add_argument('-t', '--target-lang', metavar='en|es', nargs='?',
                        help='Give a target language (overrides config)')
arg_parser.add_argument('-m', '--message', metavar='Text to translate',
                        nargs='?', help='Pass directly the actual text to '
                                        'translate as an argument (overrides'
                                        ' clipboard and selection)')
arg_parser.add_argument('-i', '--input', metavar='clipboard|selection',
                        nargs='?', help='From where the text has to be taken')
arg_parser.add_argument('-o', '--output', metavar='stdout|notify|dialog|none',
                        nargs='?', help='Where to (out)put the translation')
arg_parser.add_argument('-x', '--exchange', action='store_true',
                        help='Exchange/paste translation to clipboard')
arg_parser.add_argument('--save-config', action='store_true',
                        help='Save a config file at default (or -c given) path'
                             ', based on default or stored/saved settings.')
args = arg_parser.parse_args()

default_cfg_path = os.path.expanduser("~/.babelPy.json")
CONFIG_FILE_PATH = args.config_file if args.config_file else default_cfg_path
settings = ConfigSettings(CONFIG_FILE_PATH)
if args.save_config:
    return_code = settings.save(args)
    sys.exit(status=return_code)

SOURCE_LANG = args.source_lang if args.source_lang else "auto"
TARGET_LANG = args.target_lang if args.target_lang else settings.language

INPUT_TYPE = args.input if args.input else settings.input
if not args.message:
    try:
        # noinspection PyUnresolvedReferences
        from babelpy_utils.clipboard import push_clipboard, pull_input

        source_text = pull_input(INPUT_TYPE)
    except ImportError as exception:
        source_text = "[Error] Python module pyperclip not found!"
        print("[Error] Python module pyperclip not found!")
        print("[Error] -> {0}".format(exception))
        sys.exit(status=1)
else:
    source_text = args.message

OUTPUT_TYPE = args.output if args.output else settings.output
if platform.system() != "Linux" and OUTPUT_TYPE != "stdout":
    print("[Error] Notification and dialogs are supported only on Linux.")
    sys.exit(1)
if OUTPUT_TYPE == "notify":
    try:
        from babelpy_utils.notify import send_notification
    except ImportError:
        def send_notification():
            return "[Error] GTK+ Notify module not found!"


        print("[Error] Python GTK+ Notify module not found!")
        sys.exit(status=1)
elif OUTPUT_TYPE == "dialog":
    try:
        from babelpy_utils.dialog import show_dialog
    except ImportError:
        def show_dialog():
            return "[Error] Tkinter module not found!"


        print("[Error] Python tkinter module not found!")
        sys.exit(status=1)

TARGET_BACKEND = args.backend if args.backend else settings.backend
if TARGET_BACKEND == "yandex":
    from translation.yandex.yandex_helper import YandexHelperException, \
        YandexTranslateHelper as TranslateHelper
    from translation.yandex.yandex_translator import YandexTranslatorException

API_KEY = args.api_key if args.api_key else settings.api_key
translator = TranslateHelper(API_KEY)

try:
    if args.source_lang:
        translation = translator.translate_manual(source_text, SOURCE_LANG,
                                                  TARGET_LANG)
    else:
        translation = translator.translate_auto(source_text, TARGET_LANG)
except (YandexTranslatorException, YandexHelperException) as exception:
    print("[Error] An error occurred while requesting translation!")
    print("[Error] -> {0}".format(exception))
    sys.exit(1)

APP_PATH = os.path.dirname(os.path.realpath(__file__))
APP_ICON_PATH = APP_PATH + "/resources/icons/transClipper-outline-64.png"

if OUTPUT_TYPE == "notify":
    try:
        send_notification(APP_ID, APP_ICON_PATH, translation, TARGET_LANG)
    except ImportError as exception:
        print("[Error] Python GTK+ module Notify not found!")
        print("[Error] -> {0}".format(exception))
        sys.exit(status=1)
elif OUTPUT_TYPE == "dialog":
    try:
        show_dialog(APP_ID, source_text, translation, TARGET_LANG)
    except ImportError as exception:
        print("[Error] Python module(s) tkinter or pyperclip not found!")
        print("[Error] -> {0}".format(exception))
        sys.exit(status=1)
elif OUTPUT_TYPE == "stdout":
    print("Translated to: " + TARGET_LANG + "\n" + translation)

if args.exchange or settings.exchange:
    try:
        push_clipboard(translation)
    except ImportError as exception:
        print("[Error] Python pyperclip module not found!")
        print("[Error] -> {0}".format(exception))
        sys.exit(status=1)