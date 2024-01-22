import streamlit as st
import pandas as pd

def show_update_log():
    update_log = pd.read_excel('DATA/SOURCE DATA/update_log.xlsx')

    st.write('Update Log')
    st.table(update_log)
    return