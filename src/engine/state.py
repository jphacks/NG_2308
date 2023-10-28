from typing import TypeVar, Generic, Union, Callable

T = TypeVar('T')

#状態管理クラス。bind()で状態変更時に呼び出したい処理を登録できる。
class State(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._observers: list[Callable] = []

    def get(self):
        return self._value #値の参照はここから

    def set(self, new_value: T):
        if self._value != new_value:
            self._value = new_value #新しい値をセット
            for observer in self._observers: observer() #変更時に各observerに通知する

    def bind(self, observer):
        self._observers.append(observer)# 変更時に呼び出す為のリストに登録
