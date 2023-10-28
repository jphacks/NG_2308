"""
MacOSで実行する際は、下記のwebサイトを参考に修正が必要
https://hawk-tech-blog.com/python-notification-plyer-pyobjus-macos/
"""
import os
import glob

from plyer import notification
import simpleaudio

file_name = "default_alert.wav"

# 効果音のパスを取得する
def get_default_wav_path():
    
    # カレントディレクトリを取得する
    current_dir = os.getcwd()

    # カレントディレクトリを遡る形でファイルを検索する
    end_t = len(current_dir)
    while True:
        end_t = current_dir.rfind(os.sep, 0, end_t)
        if end_t == -1: return None
        files = glob.glob(f"{current_dir[0:end_t]}{os.sep}**{os.sep}{file_name}")
        if len(files) > 0: return files[0]

def do_popup_notify(message: str="通知内容"):
    notification.notify(
        title="15minutes",
        message=message,
        app_icon="",
        timeout=100,
    )

# ファイル名の効果音を演奏する
def play_sound(filename: str):
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    do_popup_notify("テスト")
    play_sound(get_default_wav_path())
