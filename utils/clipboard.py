import os

import pyperclip


def _pull_clipboard(): return pyperclip.paste()


def _pull_selection(): return os.popen("xsel -o").read()


def pull_input(src_input):
    return _pull_clipboard() if src_input == "clipboard" else _pull_selection()


def push_clipboard(content): pyperclip.copy(content)
