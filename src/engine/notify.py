"""
MacOSで実行する際は、下記のwebサイトを参考に修正が必要
https://hawk-tech-blog.com/python-notification-plyer-pyobjus-macos/
"""
import os
import glob

from plyer import notification
import simpleaudio

import time
import threading
import yaml
import csv

file_name = "default_alert.wav"
yaml_file = 'var/settings.yaml'
csv_file =  'var/judge.csv'

#その話題に対してアラートをすでにしたか
do_alert = False

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

        if len(files) > 0: return files[0]
def do_popup_notify(message: str="そろそろ人に聞いてみてはいかが?"):
    notification.notify(
        title="15minutes",
        message=message,
        app_icon="",
        timeout=100,
    )
#通知を行うか判定する
def notify_callback():
    global do_alert
    with open(csv_file,'r')as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)  # CSVファイルをリストに読み込み
        r_rows = list(reversed(rows))
        if r_rows[0][3] == 'False' :
            do_alert = False
        for row in r_rows:
            if row[3]=='False' : 
                if (time.time() - float(row[0])) > 900 and do_alert == False: 
                    do_popup_notify()
                    with open(yaml_file, 'r') as f:
                        settings = yaml.load(f, Loader=yaml.FullLoader)
                        if settings['is_play_sound'] :
                            play_sound(get_default_wav_path())
                        do_alert = True
                break

# ファイル名の効果音を演奏する
def play_sound(filename: str):
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=notify_callback)
        t.start()
        next_time = ((base_time - time.time()) % 30) or 30
        time.sleep(next_time)

