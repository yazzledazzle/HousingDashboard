import streamlit as st
from waitlist_trendcharts import *
from waitlist_breakdowns import *
from waitlist_latest import *
from EXTERNAL_RESOURCES import *
from ROGS_functions import *
from SHS_monthly import *
from Airbnb import *
from update_log import *

st.set_page_config(layout="wide")
goto = st.sidebar.selectbox('Select page', ['Waitlist', 'ROGS', 'SHS monthly data', 'Airbnb', 'Census', 'External resources', 'User guide'], index=0)
if goto == 'Waitlist':
    Waitlist_select = st.sidebar.selectbox('Select view', ['Latest data', 'Overall trend', 'Breakdowns'])
    if Waitlist_select == 'Latest data':
        waitlist_latest()
    elif Waitlist_select == 'Overall trend':
        waitlist_trendcharts()
    elif Waitlist_select == 'Breakdowns':
        waitlist_breakdowns()
        
elif goto == 'External resources':
    external_resources()
elif goto == 'ROGS':
    ROGS_select = st.sidebar.selectbox('Select ROGS page', ['Sector overview', 'Housing', 'Homelessness'])
    if ROGS_select == 'Sector overview':
        ROGS_sector()
    elif ROGS_select == 'Housing':
        ROGS_housing()
    elif ROGS_select == 'Homelessness':
        ROGS_homelessness()
elif goto == 'SHS monthly data':
    SHS_select = st.sidebar.selectbox('Select SHS page', ['Client groups', 'Reasons for seeking assistance'])
    if SHS_select == 'Client groups':
        SHS_client_groups()
    elif SHS_select == 'Reasons for seeking assistance':
        SHS_reasons()
elif goto == 'Airbnb':
    Airbnb_select = st.sidebar.selectbox('Select Airbnb page', ['WA total - by room type', 'Geographic filters'])
    if Airbnb_select == 'WA total - by room type':
        airbnb_wa()
    elif Airbnb_select == 'Geographic filters':
        airbnb_geo()
elif goto == 'User guide':
    show_update_log()




def sidebar():
    goto = st.sidebar.selectbox('Select page', ['Waitlist', 'ROGS', 'SHS monthly data', 'Airbnb', 'Census', 'External resources', 'Update log', 'User guide'])
    if goto == 'Waitlist':
        Waitlist_select = st.sidebar.selectbox('Select view', ['Latest data', 'Overall trend', 'Breakdowns'])
        if Waitlist_select == 'Latest data':
            waitlist_latest()
        elif Waitlist_select == 'Overall trend':
            waitlist_trendcharts()
        elif Waitlist_select == 'Breakdowns':
            waitlist_breakdowns()
            
        
    elif goto == 'External resources':
        external_resources()
    elif goto == 'ROGS':
        ROGS_select = st.sidebar.selectbox('Select ROGS page', ['Sector overview', 'Housing', 'Homelessness'])
        if ROGS_select == 'Sector overview':
            ROGS_sector()
            sidebar()
        elif ROGS_select == 'Housing':
            ROGS_housing()
        elif ROGS_select == 'Homelessness':
            ROGS_homelessness()
    elif goto == 'SHS monthly data':
        SHS_select = st.sidebar.selectbox('Select SHS page', ['Client groups', 'Reasons for seeking assistance'])
        sidebar()
        if SHS_select == 'Client groups':
            SHS_client_groups()
            sidebar()
        elif SHS_select == 'Reasons for seeking assistance':
            SHS_reasons()
    elif goto == 'Airbnb':
        Airbnb_select = st.sidebar.selectbox('Select Airbnb page', ['WA total - by room type', 'Geographic filters'])
        if Airbnb_select == 'WA total - by room type':
            airbnb_wa()
        elif Airbnb_select == 'Geographic filters':
            airbnb_geo()
    return