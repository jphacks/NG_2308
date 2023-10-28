import flet as ft

def main(page: ft.Page):
    page.title = "Flow15"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 値を動的にしたい部分のControlインスタンスを作成
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # ボタンがクリックされたら
    def on_toggle(e):
        b.data += 1
        txt_number.value = str(b.data)
        page.update()

    b = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=on_toggle, data=0
    )

    page.add(b, txt_number)


ft.app(target=main)