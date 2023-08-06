import streamlit as st
import pandas as pd



option = st.selectbox(
    'Which number do you like best?',
     [1,2,3,4,5])

'You selected: ', option