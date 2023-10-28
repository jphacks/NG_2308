"""
MacOSで実行する際は、下記のwebサイトを参考に修正が必要
https://hawk-tech-blog.com/python-notification-plyer-pyobjus-macos/
"""
from plyer import notification

def do_popup_notify(message: str="通知内容"):
    notification.notify(
        title="15minutes",
        message=message,
        app_icon="",
        timeout=100,
    )

if __name__ == "__main__":
    do_popup_notify("テスト")