import simpleaudio, os, glob

file_name = "default_alert.wav"

# 効果音のパスを取得する
def get_default_wav_path():
    
    # カレントディレクトリを取得する
    current_dir = os.getcwd()

    # カレントディレクトリを遡る形でファイルを検索する
    end_t = len(current_dir)
    while True:
        end_t = current_dir.rfind("/", 0, end_t)
        if end_t == -1: return None
        files = glob.glob("{}/**/{}".format(current_dir[0:end_t], file_name))
        if len(files) > 0: return files[0]


# ファイル名の効果音を演奏する
def play_sound(filename: str):
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    play_sound(get_default_wav_path())