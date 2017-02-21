import time
import tkinter
from abc import ABC, abstractmethod

import gi

gi.require_version('Notify', '0.7')
from gi.repository import Notify


class TranslateNotifier(ABC):
    """TranslateNotifier abstract class representing notifier functionality"""

    @abstractmethod
    def __init__(self, app_id, icon_path):
        """Constructor for TranslateNotifier"""
        self.app_id = app_id
        self.icon_path = icon_path

    @abstractmethod
    def notify(self, title, message, language):
        pass


class TkDialogNotifier(tkinter.Frame):
    """TkDialogNotifier - TkDialog showing translation"""

    def __init__(self, master=None):
        super().__init__(master)
        self.root_tk = master
        self.pack()
        self._setup_widgets()

    def _setup_widgets(self):
        self.text_box_source = tkinter.Text(self, width=40, height=5)
        self.text_box_translated = tkinter.Text(self, width=40, height=5)
        self.quit_button = tkinter.Button(self, text="QUIT", fg="red",
                                          command=self.root_tk.destroy)
        self.quit_button.pack(side="bottom")
        self.action_button = tkinter.Button(self)
        self.action_button["text"] = "Copy to clipboard"
        self.action_button["command"] = self.action_button_callback
        self.action_button.pack(side="bottom")

    def action_button_callback(self):
        from utils.clipboard import push_clipboard
        push_clipboard(self.text_box_translated.get("1.0", tkinter.END))
        self.action_button["text"] = "Copied to clipboard!"
        time.sleep(3)
        self.action_button["text"] = "Copy to clipboard"

    def set_source_text(self, message):
        self.text_box_source.insert(tkinter.INSERT, message)
        self.text_box_source.pack(side="left")
        self.text_box_source.config(state=tkinter.DISABLED)

    def set_translated_text(self, message):
        self.text_box_translated.insert(tkinter.INSERT, message)
        self.text_box_translated.pack(side="left")
        self.text_box_translated.config(state=tkinter.DISABLED)

    def set_action_button_text(self, button_text):
        self.action_button["text"] = button_text

    @staticmethod
    def show_dialog(app_id, src_message, translation, target_language):
        root_tk = tkinter.Tk()
        root_tk.title(app_id + " - Translated to: " + target_language)
        root_tk.minsize(width=100, height=20)
        tk_dialog = TkDialogNotifier(master=root_tk)
        tk_dialog.set_source_text(src_message)
        tk_dialog.set_translated_text(translation)
        tk_dialog.mainloop()


class LinuxNotifier(TranslateNotifier):
    """LinuxNotifier class handles linux notifications"""

    def __init__(self, app_id, icon_path):
        """Constructor for LinuxNotifier"""
        super().__init__(app_id, icon_path)
        Notify.init(app_id)
        self.icon_path = icon_path

    def notify(self, message, title, language):
        notify_title = "<b>Translated to: " + language + "</b>"
        Notify.Notification.new(notify_title, message, self.icon_path).show()
        Notify.uninit()


class NotifyHelper(TranslateNotifier):
    """NotifyHelper class that helps handling notifications between systems"""

    def __init__(self, app_id, icon_path):
        """Constructor for NotifyHelper"""
        super().__init__(app_id, icon_path)

    def notify(self, message, title, language):
        LinuxNotifier(self.app_id, self.icon_path).notify(message,
                                                          title,
                                                          language)
