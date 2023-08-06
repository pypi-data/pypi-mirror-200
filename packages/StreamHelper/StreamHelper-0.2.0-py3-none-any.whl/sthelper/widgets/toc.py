import streamlit as st
from typing import List, Tuple

def build_TOC(headers: List[Tuple[str, str]]):
    '''

    :param headers: a list of (header type, header name). e.g. ('h1', 'my header 1')
    :return:
    '''
    # create a hyperlink that navigates to an internal section of the Streamlit app

    for hn, h_name in headers:
        if hn == 'h1':
            intent = ''
        elif hn == 'h2':
            intent = '&nbsp;&nbsp;'
        elif hn == 'h3':
            intent = '&nbsp;&nbsp;'*2
        elif hn == 'h4':
            intent = '&nbsp;&nbsp;'*3
        elif hn == 'h5':
            intent = '&nbsp;&nbsp;'*4
        else:
            raise ValueError(f"Not supported header type: {hn}.")

        nav = h_name.replace(' ','-').lower()
        st.markdown(
            f'''{intent} <a style="color: #999999; text-decoration: underline" href="#{nav}">{h_name}</a>''',
            unsafe_allow_html=True)

if __name__ == '__main__':
    build_TOC([
        ('h1','Header1'),
        ('h3','subheader 1'),
        ('h1','Header2')
    ])