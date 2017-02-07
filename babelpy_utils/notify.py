import gi

gi.require_version('Notify', '0.7')
from gi.repository import Notify


def send_notification(app_id, icon_path, message, language):
    title = "<b>Translated to: " + language + "</b>"
    Notify.init(app_id)
    Notify.Notification.new(title, message, icon_path).show()
    Notify.uninit()
