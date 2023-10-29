import flet as ft
import os
import glob
import yaml

# ディレクトリとファイルパス
file_path = 'var/settings.yaml'
directory_path = 'var'
log_path = "var/judge.csv"

# ディレクトリが存在しない場合、作成する
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# settings.yamlファイルが存在しない場合、新しいファイルを作成
if not os.path.exists(file_path):
    default_settings = {'is_running': False, 'is_play_sound': True}
    with open(file_path, 'w') as file:
        yaml.dump(default_settings, file)
else:
    # settings.yamlファイルが存在する場合、is_runningを上書き
    with open(file_path, 'r') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
        settings['is_running'] = False
    with open(file_path, 'w') as file:
        yaml.dump(settings, file)


# 監視モードを定義
monitor_mode = False

# 音の有無を設定
sound_mode = True

# カレントディレクトリを遡る形で指定ファイルを取得
def find_file(file_name):
    current_dir = os.getcwd()
    end_t = len(current_dir)
    while True:
        files = glob.glob(f"{current_dir[0:end_t]}{os.sep}resources{os.sep}animation{os.sep}{file_name}")
        if len(files) > 0: return files[0]
        end_t = current_dir.rfind(os.sep, 0, end_t)
        if end_t == -1: return None

# イール君のパスを取得
animation_sleep = find_file("sleeping.gif")
animation_awake = find_file("working.gif")

# イール君の画像を設定
eel_img = ft.Image(
    src=animation_sleep,
    width=100,
)

def main(page: ft.Page):

    # 監視ボタンを定義
    monitor_btn = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE,
        icon_color=ft.colors.GREEN,
        icon_size=130,
    )

    # 監視モードをクリックしたら
    def monitor_clicked(e):
        global monitor_mode, eel_img
        if not monitor_mode:
            monitor_mode = True
            monitor_btn.icon = ft.icons.PAUSE_CIRCLE
            monitor_btn.icon_color = ft.colors.PINK
            eel_img.src = animation_awake
            #監視モードのonをyamlに記載
            with open(file_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
                settings['is_running'] = True
            with open(file_path, 'w') as file:
                yaml.dump(settings, file)
            # ログファイルの中身を初期化
            with open(log_path, mode='w', newline='') as file:
                file.truncate(0)
        else:
            monitor_mode = False
            monitor_btn.icon = ft.icons.PLAY_CIRCLE
            monitor_btn.icon_color = ft.colors.GREEN
            eel_img.src = animation_sleep
            #監視モードのoffをyamlに記載
            with open(file_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
                settings['is_running'] = False
            with open(file_path, 'w') as file:
                yaml.dump(settings, file)

        monitor_btn.update()
        eel_img.update()

    # クリック時の処理を定義
    monitor_btn.on_click=monitor_clicked

    # 設定ボタンを定義
    setting_btn = ft.IconButton(
        icon=ft.icons.SETTINGS,
        icon_color="#333333",
        icon_size=30,
        on_click=lambda _:page.go(f"{os.sep}settings")
    )

    # 戻るボタンを定義
    return_btn = ft.IconButton(
        icon=ft.icons.HOME,
        icon_color="#333333",
        icon_size=30,
        on_click=lambda _:page.go(f"{os.sep}")
    )

    # 音声ボタンをクリックしたら
    def sound_clicked(e):
        global sound_mode
        if not sound_mode:
            sound_mode = True
            #音声のonをyamlに記載
            with open(file_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
            settings['is_play_sound'] = True
            with open(file_path, 'w') as file:
                yaml.dump(settings, file)
        else:
            sound_mode = False
            #音声のoffをyamlに記載
            with open(file_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
                settings['is_play_sound'] = False
            with open(file_path, 'w') as file:
                yaml.dump(settings, file)

    # トップページ
    def view_root():
        return ft.View(f"{os.sep}", [
            ft.Column([
                ft.Container(
                    content=setting_btn,
                    alignment=ft.alignment.center_right
                ),
                ft.Column([
                    ft.Container(
                        content=monitor_btn,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=eel_img,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=-320)
                    ),
                ])
            ])
        ])

    # 設定ページ
    def view_settings():
        return ft.View(f"{os.sep}settings", [
            ft.Column([
                ft.Container(
                    content=return_btn,
                    alignment=ft.alignment.center_right
                ),
                ft.Container(
                    ft.Row([
                        ft.Switch(on_change=sound_clicked, value=True),
                        ft.Text("Play Sound"),
                    ]),
                    margin=ft.margin.only(left=30)
                ),
            ], alignment=ft.alignment.center
            )
        ])


    # ルーター
    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        page.views.clear()
        if troute.match(f"{os.sep}"):
            page.views.append(view_root())
        elif troute.match(f"{os.sep}settings"):
            page.views.append(view_settings())
        page.update()


    # ルーターを定義
    page.on_route_change = route_change

    page.title = "Fifteel"   # タイトル
    page.window_width = 300   # 幅
    page.window_height = 300  # 高さ
    page.window_always_on_top = True  # ウィンドウを最前面に固定
    page.window_center()  # ウィンドウをデスクトップの中心に移動

    # 初期ページを開く
    page.go(f"{os.sep}")


if __name__ == "__main__":
    ft.app(target=main)

