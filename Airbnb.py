import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def airbnb_wa():
    df_wa_total = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_WAtotals.csv')
    df_wa_total['date'] = pd.to_datetime(df_wa_total['date'], format='%Y-%m-%d', errors='coerce')
    df_wa_total = df_wa_total.sort_values(by='date', ascending=True)
    #rename count_listings to count
    df_wa_total = df_wa_total.rename(columns={'count_listings': 'count'})
    #date to string
    df_wa_total['date'] = df_wa_total['date'].astype(str)
    df_geo = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_allgeo.csv')
    #rename SA2_NAME_2016 to SA2, SA3_NAME_2016 to SA3, SA4_NAME_2016 to SA4
    df_geo = df_geo.rename(columns={'SA2_NAME_2016':'SA2', 'SA3_NAME_2016':'SA3', 'SA4_NAME_2016':'SA4', 'id_count': 'count'})

    fig = go.Figure()
    for room_type in df_wa_total['room_type'].unique():
        df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
        fig.add_trace(go.Bar(x=df_room_type['date'].astype(str), y=df_room_type['count'], name=room_type))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
    fig.update_layout(title='Number of Airbnb listings in WA by type', xaxis_title='', yaxis_title='Number of listings')
    #decrease bottom margin
    fig.update_layout(margin=dict(b=0))
    st.plotly_chart(fig)

    #plot median price
    fig2 = go.Figure()
    for room_type in df_wa_total['room_type'].unique():
        df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
        fig2.add_trace(go.Bar(x=df_room_type['date'].astype(str), y=df_room_type['price_median'], name=room_type))
    fig2.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig2.update_layout(title='Median price of Airbnb listings in WA', xaxis_title='', yaxis_title='Median price ($)')
    st.plotly_chart(fig2)

    #plot mean price
    fig3 = go.Figure()
    for room_type in df_wa_total['room_type'].unique():
        df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
        fig3.add_trace(go.Bar(x=df_room_type['date'].astype(str), y=df_room_type['price_mean'], name=room_type))
    fig3.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig3.update_layout(title='Mean price of Airbnb listings in WA', xaxis_title='', yaxis_title='Mean price ($)')
    st.plotly_chart(fig3)

    #plot median availability
    fig4 = go.Figure()
    for room_type in df_wa_total['room_type'].unique():
        df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
        fig4.add_trace(go.Bar(x=df_room_type['date'].astype(str), y=df_room_type['availability_365_median'], name=room_type))
    fig4.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig4.update_layout(title='Median availability of Airbnb listings in WA', xaxis_title='', yaxis_title='Median availability (days)')
    st.plotly_chart(fig4)
    #plot mean availability
    fig5 = go.Figure()
    for room_type in df_wa_total['room_type'].unique():
        df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
        fig5.add_trace(go.Bar(x=df_room_type['date'].astype(str), y=df_room_type['availability_365_mean'], name=room_type))
    fig5.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig5.update_layout(title='Mean availability of Airbnb listings in WA', xaxis_title='', yaxis_title='Mean availability (days)')
    st.plotly_chart(fig5)

    return

def airbnb_geo():
    df_wa_total = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_WAtotals.csv')
    df_wa_total['date'] = pd.to_datetime(df_wa_total['date'], format='%Y-%m-%d', errors='coerce')
    df_wa_total = df_wa_total.sort_values(by='date', ascending=True)
    #rename count_listings to count
    df_wa_total = df_wa_total.rename(columns={'count_listings': 'count'})
    #date to string
    df_wa_total['date'] = df_wa_total['date'].astype(str)
    df_geo = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_allgeo.csv')
    #rename SA2_NAME_2016 to SA2, SA3_NAME_2016 to SA3, SA4_NAME_2016 to SA4
    df_geo = df_geo.rename(columns={'SA2_NAME_2016':'SA2', 'SA3_NAME_2016':'SA3', 'SA4_NAME_2016':'SA4', 'id_count': 'count'})

    st.markdown(f'#### Geographic filters')



    select_geo = st.radio('Select geography filter type:', ['Census areas (multi-level)', 'Federal electorate', 'LGA'], index=0)
    col1, col2, col3 = st.columns(3)

    if select_geo == 'Census areas (multi-level)':

        with col1:
            SA4 = st.multiselect('Select SA4', df_geo['SA4'].unique())
            if SA4:
                df_geo_fil = df_geo[df_geo['SA4'].isin(SA4)]
        with col2:
            if SA4:
                SA3 = st.multiselect('Select SA3', df_geo_fil['SA3'].unique(), default=df_geo_fil['SA3'].unique())
                df_geo_fil = df_geo_fil[df_geo_fil['SA3'].isin(SA3)]
            else:
                SA3 = st.multiselect('Select SA3', df_geo['SA3'].unique())
                if SA3:
                    df_geo_fil = df_geo[df_geo['SA3'].isin(SA3)]
                    if len(SA3) == len(df_geo['SA3'].unique()):
                        df_geo_fil = df_geo_fil.groupby(['date', 'room_type', 'SA4']).agg({'count': 'sum', 'price_mean': 'mean', 'availability_365_mean': 'mean', 'price_median': 'median', 'availability_365_median': 'median'}).reset_index()

        with col3:
            if SA3:
                SA2 = st.multiselect('Select SA2', df_geo_fil['SA2'].unique(), default=df_geo_fil['SA2'].unique())
                df_geo_fil = df_geo_fil[df_geo_fil['SA2'].isin(SA2)]
            else:
                SA2 = st.multiselect('Select SA2', df_geo['SA2'].unique())
                if SA2:
                    df_geo_fil = df_geo[df_geo['SA2'].isin(SA2)]
                    #if all selected, groupby date, room_type, SA3, sum count, mean price, mean availability_365, median price, median availability_365
                    if len(SA2) == len(df_geo['SA2'].unique()):
                        df_geo_fil = df_geo_fil.groupby(['date', 'room_type', 'SA3']).agg({'count': 'sum', 'price_mean': 'mean', 'availability_365_mean': 'mean', 'price_median': 'median', 'availability_365_median': 'median'}).reset_index()

    elif select_geo == 'Federal electorate':
        fed_electorate = st.multiselect('Select federal electorate', df_geo['electorate'].unique())
        if fed_electorate:
            df_geo_fil = df_geo[df_geo['electorate'].isin(fed_electorate)]
            df_geo_fil = df_geo_fil.groupby(['date', 'room_type', 'electorate']).agg({'count': 'sum', 'price_mean': 'mean', 'availability_365_mean': 'mean', 'price_median': 'median', 'availability_365_median': 'median'}).reset_index()

    elif select_geo == 'LGA':
        LGA = st.multiselect('Select LGA', df_geo['lgaregion'].unique())
        if LGA:
            df_geo_fil = df_geo[df_geo['lgaregion'].isin(LGA)]
            df_geo_fil = df_geo_fil.groupby(['date', 'room_type', 'lgaregion']).agg({'count': 'sum', 'price_mean': 'mean', 'availability_365_mean': 'mean', 'price_median': 'median', 'availability_365_median': 'median'}).reset_index()


    try:
        room_type = st.multiselect('Select room type', df_geo_fil['room_type'].unique(), default=df_geo_fil['room_type'].unique())
        if room_type:
            df_geo_fil = df_geo_fil[df_geo_fil['room_type'].isin(room_type)]
    except:
        room_type = st.multiselect('Select room type', df_geo['room_type'].unique(), default=df_geo['room_type'].unique())
        if room_type:
            df_geo_fil = df_geo[df_geo['room_type'].isin(room_type)]
        
    fig = go.Figure()
    #hovertext is sum of all count for date, room_type

    for room_type in df_geo_fil['room_type'].unique():
        
        df_room_type = df_geo_fil[df_geo_fil['room_type'] == room_type]
        fig.add_trace(go.Bar(x=df_geo_fil['date'], y=df_geo_fil['count'], name=room_type))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    fig.update_layout(title='Number of Airbnb listings in area by type', xaxis_title='', yaxis_title='Number of listings')
    #decrease bottom margin
    fig.update_layout(margin=dict(b=0))
    st.markdown(f'*Hover values over bars in geographic filtered chart do not currently reflect single total for date, room type - currently showing multiple points for each suburb in area, to be corrected*')
    st.plotly_chart(fig)
    
    #plot median price
    fig2 = go.Figure()
    for room_type in df_geo_fil['room_type'].unique():
        df_room_type = df_geo_fil[df_geo_fil['room_type'] == room_type]
        fig2.add_trace(go.Bar(x=df_room_type['date'], y=df_room_type['price_median'], name=room_type))
    fig2.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig2.update_layout(title='Median price of Airbnb listings in area', xaxis_title='', yaxis_title='Median price ($)')
    st.plotly_chart(fig2)

    #plot mean price
    fig3 = go.Figure()
    for room_type in df_geo_fil['room_type'].unique():
        df_room_type = df_geo_fil[df_geo_fil['room_type'] == room_type]
        fig3.add_trace(go.Bar(x=df_room_type['date'], y=df_room_type['price_mean'], name=room_type))
    fig3.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig3.update_layout(title='Mean price of Airbnb listings in area', xaxis_title='', yaxis_title='Mean price ($)')
    st.plotly_chart(fig3)

    #plot median availability
    fig4 = go.Figure()
    for room_type in df_geo_fil['room_type'].unique():
        df_room_type = df_geo_fil[df_geo_fil['room_type'] == room_type]
        fig4.add_trace(go.Bar(x=df_room_type['date'], y=df_room_type['availability_365_median'], name=room_type))
    fig4.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig4.update_layout(title='Median availability of Airbnb listings in area', xaxis_title='', yaxis_title='Median availability (days)')
    st.plotly_chart(fig4)
    #plot mean availability
    fig5 = go.Figure()
    for room_type in df_geo_fil['room_type'].unique():
        df_room_type = df_geo_fil[df_geo_fil['room_type'] == room_type]
        fig5.add_trace(go.Bar(x=df_room_type['date'], y=df_room_type['availability_365_mean'], name=room_type))
    fig5.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})
    fig5.update_layout(title='Mean availability of Airbnb listings in area', xaxis_title='', yaxis_title='Mean availability (days)')
    st.plotly_chart(fig5)
    return

