import gi

gi.require_version('Notify', '0.7')
from gi.repository import Notify

from notification.notify import TranslateNotifier


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