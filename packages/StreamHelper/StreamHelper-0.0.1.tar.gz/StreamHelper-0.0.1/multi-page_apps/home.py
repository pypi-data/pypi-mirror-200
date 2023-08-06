import streamlit as st
markdown = '''# 个人服务器
## 已经实现了的
![](https://i.imgur.com/Nmg8ssD.png)

## Reproduction
<iframe width="720" height="405" frameborder="0" src="https://www.ixigua.com/iframe/7143320100505027084?autoplay=0" referrerpolicy="unsafe-url" allowfullscreen></iframe>

'''
st.markdown(markdown,unsafe_allow_html=True)