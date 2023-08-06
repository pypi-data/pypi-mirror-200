import streamlit as st
from typing import Dict, Callable

class OpenSession:
    def __init__(self, page_map: Dict[str, Callable[[], None]], current_page:str = 'home') -> None:
        super().__init__()

        self.__page_map__ = page_map
        self.init('current_page',current_page)

    def get_current_page(self) -> str:
        return self.get('current_page')

    def get_page_map(self) -> dict:
        return self.__page_map__

    def init(self, key: str, value):
        if key not in st.session_state:
            st.session_state[key] = value

    def update(self, key: str, value):
        st.session_state[key] = value

    def has(self, key: str):
        return key in self.to_dict().keys()

    def get(self, key: str):
        tmp = self.to_dict()
        if key in tmp.keys():
            return tmp[key]
        else:
            return None

    def summary(self):
        tmp = self.to_dict()
        num = len(tmp.keys())
        ret = f'''There are {num} variables:\n\n'''
        for k in tmp.keys():
            v = tmp[k]
            ret += f'''"{k}": {v}\n\n'''
        return ret

    def to_dict(self):
        return st.session_state.to_dict()

    def render(self):
        page = self.get_current_page()
        page_func = self.get_page_map()[page]
        if page_func is not None:
            page_func()


    def go_to_page(self,page:str):
        if page not in self.__page_map__.keys():
            print('\033[31m' + f'There is not {page} page in the current page map.' + '\033[0m')
        else:
            self.update('current_page', page)

