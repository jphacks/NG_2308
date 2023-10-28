import flet as ft

# 監視モードを定義
monitor_mode = False

def main(page: ft.Page):

    # 監視ボタンを定義
    monitor_btn = ft.IconButton(
        icon=ft.icons.PAUSE_CIRCLE,
        icon_color=ft.colors.PINK,
        icon_size=100,
    )

    # 監視モードをクリックしたら
    def monitor_clicked(e):
        global monitor_mode
        if not monitor_mode:
            monitor_mode = True
            monitor_btn.icon = ft.icons.PLAY_CIRCLE
            monitor_btn.icon_color = ft.colors.GREEN
        else:
            monitor_mode = False
            monitor_btn.icon = ft.icons.PAUSE_CIRCLE
            monitor_btn.icon_color = ft.colors.PINK
        monitor_btn.update()
    
    # クリック時の処理を定義
    monitor_btn.on_click=monitor_clicked

    # 設定ボタンを定義
    setting_btn = ft.IconButton(
        icon=ft.icons.SETTINGS,
        icon_color="#333333",
        icon_size=30,
        on_click=lambda _:page.go("/settings")
    )

    # 戻るボタンを定義
    return_btn = ft.IconButton(
        icon=ft.icons.HOME,
        icon_color="#333333",
        icon_size=30,
        on_click=lambda _:page.go("/")
    )

    # トップページ
    def view_root():
        return ft.View("/", [
            ft.Column([
                ft.Container(
                    content=setting_btn,
                    alignment=ft.alignment.center_right
                ),
                ft.Container(
                    content=monitor_btn,
                    margin=20,
                    alignment=ft.alignment.center
                ),
            ])
        ])
    

    # 設定ページ
    def view_settings():
        return ft.View("/settings", [
            ft.Column([
                ft.Container(
                    content=return_btn,
                    alignment=ft.alignment.center_right
                ),
                ft.Container(
                    content=ft.Text("this is a settings page"),
                    alignment=ft.alignment.center_left
                ),
            ])
        ])
    

    # ルーター
    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        page.views.clear()
        if troute.match("/"):
            page.views.append(view_root())
        elif troute.match("/settings"):
            page.views.append(view_settings())
        page.update()


    # ルーターを定義
    page.on_route_change = route_change

    page.title = "Test App"   # タイトル
    page.window_width = 300   # 幅
    page.window_height = 300  # 高さ
    page.window_always_on_top = True  # ウィンドウを最前面に固定
    page.window_center()  # ウィンドウをデスクトップの中心に移動

    # 初期ページを開く
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)