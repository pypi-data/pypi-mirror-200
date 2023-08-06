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


def add_new_row(data:dict):
    # data = dict(
    #     email=tmp['email'],
    #     e1_relevance=tmp['e1_relevance'],
    #     e1_coherence=tmp['e1_coherence'],
    #     e1_accuracy=tmp['e1_accuracy'],
    #     e2_relevance=tmp['e2_relevance'],
    #     e2_coherence=tmp['e2_coherence'],
    #     e2_accuracy=tmp['e2_accuracy'],
    # )
    columns_str = ", ".join(data.keys())
    new_values_str = ", ".join([f"\'{str(x)}\'" for x in data.values()])
    query = f'INSERT INTO SHEET ({columns_str}) VALUES ({new_values_str})'
    run_query(query)