# streamlit_app.py
import streamlit as st
from shillelagh.backends.apsw.db import connect


def run_query(query):
    '''

    Args:
        query: example: 'SELECT * FROM SHEET'. "SHEET" will be replaced by the gsheet url internally.

    Returns: query results

    '''
    cursor = __login_to_google__()
    sheet_url = st.secrets["private_gsheets_url"]
    query = query.replace('SHEET',f'''"{sheet_url}"''')
    dataset = cursor.execute(query)
    return dataset


def __login_to_google__():
    print("\n\n##########################\n\n")
    print("Login to Google API")

    connect_args = {
        "path": ":memory:",
        "adapters": "gsheetsapi",
        "adapter_kwargs": {
        "gsheetsapi": {
                           "service_account_info": {
                               **st.secrets["gcp_service_account"]
                           }
                       }
                   }
    }

    conn = connect(**connect_args)
    cursor = conn.cursor()
    print("Login done.")
    return cursor


def get_whole_dataset():
    query = f'SELECT * FROM SHEET'
    dataset = run_query(query)
    return dataset

