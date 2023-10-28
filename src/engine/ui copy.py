import flet as ft
from state import State
#※今回はグローバルステート化したが、本来はStoreクラスを用意して格納したり引数で渡すのが望ましい
text = State('')

class InfoAria(ft.UserControl):
    def __init__(self):
        super().__init__(self)
        self.text_len_label = ft.Text('文字数:', size=20)
        self.text_val_label = ft.Text('テキストボックスに「」と入力されています。')
        #データバインディング。変更時にon_change_handlerメソッドが呼び出される
        text.bind(self.on_change_handler)

    def on_change_handler(self):
        value = text.get()
        self.text_len_label.value = f'文字数:{len(value)}'
        self.text_val_label.value = f'テキストボックスに「{value}」と入力されています。'
        self.text_len_label.update()
        self.text_val_label.update()

    def build(self):
        return ft.Column([self.text_len_label, self.text_val_label])

def main(page: ft.Page):
    page.title = "Flet example"
    info_aria = InfoAria()
    text_box = ft.TextField(on_change=lambda e: text.set(e.control.value))
    
    page.add(ft.Column([text_box, info_aria]))

ft.app(target=main)