import streamlit as st
# Widgets can also be accessed by key, if you choose to specify a string to use as the unique key for the widget:
st.text_input("Your name", key="name")

# You can access the value at any point with:
name = st.session_state.name
name
print(name)