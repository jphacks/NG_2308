# engineサーバー

サーバー起動方法: `$ uvicorn server:app --host 0.0.0.0 --reload --port 8000`

Macの場合，以下の対応が必要．

`venv/lib/python3.11/site-packages/plyer/platforms/macosx/notification.py`を開いて，以下に置き換え．
```python
'''
Module of MacOS API for plyer.notification.
'''

from plyer.facades import Notification

import os

class OSXNotification(Notification):
    '''
    Implementation of MacOS notification API.
    '''

    def _notify(self, **kwargs):
        title = kwargs.get('title', '')
        message = kwargs.get('message', '')
        app_name = kwargs.get('app_name', '')
        sound_name = 'default'
        # app_icon, timeout, ticker are not supported (yet)

        title_text = f'with title "{title}"' if title != '' else ''
        subtitle_text = f'subtitle "{app_name}"' if app_name != '' else ''
        soundname_text = f'sound name "{sound_name}"'

        notification_text = f'display notification "{message}" {title_text} {subtitle_text} {soundname_text}'
        os.system(f"osascript -e '{notification_text}'")

def instance():
    '''
    Instance for facade proxy.
    '''
    return OSXNotification()
```

[参考](https://hawk-tech-blog.com/python-notification-plyer-pyobjus-macos/)
