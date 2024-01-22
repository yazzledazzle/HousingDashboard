import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def SHS_reasons():
    # Read the data
    df = pd.read_csv('DATA/PROCESSED DATA/SHS/Long_Form/SHS_Reasons_Long_Form.csv') 

    # Data preprocessing
    df['MEASURE'] = df['MEASURE'].fillna('Persons')  # Replace NaN in MEASURE with 'Persons'
    df = df.rename(columns={'REASON FOR SEEKING ASSISTANCE': 'REASON'})  # Rename column for ease of use

    df_latest_date = df[df['DATE'] == df['DATE'].max()]
    latest_date = df_latest_date['DATE'].max()
    df_latest_date = df_latest_date[df_latest_date['MEASURE'] == 'Persons']
    df_latest_total = df_latest_date[df_latest_date['REASON'] == 'Total clients']
    #drop columns REASON, MONTH, GROUP
    df_latest_total = df_latest_total.drop(columns=['REASON', 'MONTH', 'GROUP', 'MEASURE', 'DATE'])
    df_latest_reasons = df_latest_date[df_latest_date['REASON'] != 'Total clients']
    #drop columns MONTH, GROUP, MEASURE
    df_latest_reasons = df_latest_reasons.drop(columns=['MONTH', 'GROUP', 'MEASURE', 'DATE'])
    #join df_latest_total to df_latest_reasons on DATE, STATE, MEASURE
    df_latest_reasons = df_latest_reasons.merge(df_latest_total, on=['STATE'])
    #rename VALUE_x = VALUE, Value_y = Total clients
    df_latest_reasons = df_latest_reasons.rename(columns={'VALUE_x': 'VALUE', 'VALUE_y': 'Total clients'})
    #calculate proportion
    df_latest_reasons['proportion'] = (df_latest_reasons['VALUE'] / df_latest_reasons['Total clients'])*100
    #drop Total clients
    df_latest_reasons = df_latest_reasons.drop(columns=['Total clients'])
    nat_reasons = df_latest_reasons[df_latest_reasons['STATE'] == 'National']
    nat_reasons = nat_reasons.groupby('REASON').sum().reset_index().sort_values(by='proportion', ascending=False)
    top_reasons = nat_reasons['REASON'].head(3).tolist()
    wa_reasons = df_latest_reasons[df_latest_reasons['STATE'] == 'WA']
    wa_reasons = wa_reasons.groupby('REASON').sum().reset_index().sort_values(by='VALUE', ascending=False)
    top_reasons_wa = wa_reasons['REASON'].head(3).tolist()
    #combine top reasons for WA and National
    top_reasons = top_reasons + top_reasons_wa
    top_reasons = list(dict.fromkeys(top_reasons))


    #drop df_latest_reasons rows where REASON not in top_reasons
    df_latest_reasons = df_latest_reasons[df_latest_reasons['REASON'].isin(top_reasons)]
    df_latest_reasons_prop = df_latest_reasons
    #drop VALUE
    df_latest_reasons_prop = df_latest_reasons_prop.drop(columns=['VALUE'])
    df_latest_reasons_count = df_latest_reasons
    #drop proportion
    df_latest_reasons_count = df_latest_reasons_count.drop(columns=['proportion'])

    #pivot so each STATE is a column
    df_top_proportion = df_latest_reasons_prop.pivot_table(index=['STATE'], columns='REASON', values='proportion').reset_index()


    #latest date as mmmm yyyy
    latest_date = pd.to_datetime(latest_date, format='%Y-%m-%d').strftime('%B %Y')

    st.markdown(f'Source: <a href="https://www.aihw.gov.au/reports/homelessness-services/specialist-homelessness-services-monthly-data/data">Australian Institute of Health and Welfare - Specialist homelessness services, monthly data - last updated {latest_date} </a>', unsafe_allow_html=True)

    states = st.multiselect('Show', ['National', 'WA', 'NSW', 'Vic', 'Qld', 'SA', 'Tas', 'NT', 'ACT'], default=['National', 'WA', 'NSW', 'Vic', 'Qld', 'SA', 'Tas', 'NT', 'ACT'])

    #for each reason, category bar chart - proportion on y, state on x
    fig = go.Figure()
    #filter df_top_proportion by states
    df_top_proportion = df_top_proportion[df_top_proportion['STATE'].isin(states)]
    for reason in top_reasons:
        fig.add_trace(go.Bar(x=df_top_proportion['STATE'], y=df_top_proportion[reason], name=reason))
    fig.update_layout(barmode='group', xaxis={'categoryorder':'array', 'categoryarray': states})
    fig.update_layout(title={'text': 'Proportion of clients reporting a top reason for seeking assistance', 'x': 0.5, 'xanchor': 'center'})
    fig.update_layout(legend={'title': 'Reason for Seeking Assistance'})
    #y label % of clients
    fig.update_layout(yaxis={'title': '% of clients'})

    st.plotly_chart(fig)
    return

def SHS_client_groups():
    df = pd.read_csv('DATA/PROCESSED DATA/SHS/SHS_Client_Groups.csv')
    #column names to uppercase
    df.columns = df.columns.str.upper()
    if 'MONTH' in df.columns:
        df['DATE'] = '20' + df['MONTH'].str[3:5] + '-' + df['MONTH'].str[0:3] + '-01'
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%b-%d')
        df['DATE'] = df['DATE'] + pd.offsets.MonthEnd(0)
    population = pd.read_csv('DATA/PROCESSED DATA/Population/Population_State_Total_monthly.csv')
    population['DATE'] = pd.to_datetime(population['DATE'], format='%d/%m/%Y', dayfirst=True)
    #sort date ascending
    population = population.sort_values(by='DATE', ascending=True)
    regions = df.columns[3:12]
    print(regions)
    #Date is yyyy-mm-dd
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d', errors='coerce')
    df = df.sort_values(by='DATE', ascending=True)

    latest_date = df['DATE'].max()



    latest_date = pd.to_datetime(latest_date, format='%Y-%m-%d').strftime('%B %Y')
    df_tot = df[df['SEX'] == 'Total']
    #join df and population on DATE
    df_tot = pd.merge(df_tot, population, on='DATE', how='left')
    #forward fill any Nan columns
    df_tot = df_tot.fillna(method='ffill')

    st.markdown(f'Source: <a href="https://www.aihw.gov.au/reports/homelessness-services/specialist-homelessness-services-monthly-data/data">Australian Institute of Health and Welfare - Specialist homelessness services, monthly data - last updated {latest_date} </a>', unsafe_allow_html=True)



    per10k ={}

    for region in regions:
        region_per_10k = f'{region}_PER_10k'
        per10k[region] = region_per_10k
        
    propnat = {}
    for region in regions:
        region_prop_nat = f'{region}_PROPORTION_OF_NATIONAL'
        propnat[region] = region_prop_nat

    groups = df['CLIENT GROUP'].unique()
    groups = groups.tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        view = st.radio('Select view', ['Number of clients', 'Number of clients per 10,000 people'], index=0)
    if view == 'Number of clients per 10,000 people':
        #remove 'Number of nights in short-term/emergency accommodation' from groups
        groups.remove('Number of nights in short-term/emergency accommodation')




    with col2:
        region = st.selectbox('Select region', regions, index=3)

    group = st.selectbox('Select client group', groups, index=7)
    df = df[df['CLIENT GROUP'] == group]
    df_tot = df_tot[df_tot['CLIENT GROUP'] == group]
    fig = go.Figure()
    if view == 'Number of clients':
        with col3:
            sex = st.radio('Sex breakdown', ['On', 'Off'])
    else:
        sex  = 'Off'
    df_fem = df[df['SEX'] == 'Female']
    df_mal = df[df['SEX'] == 'Male']
    if view == 'Number of clients':
        xvalfem = df_fem['DATE']
        xvalmal = df_mal['DATE']
        xvaltot = df_tot['DATE']
        yvalfem = df_fem[region]
        yvalmal = df_mal[region]
        yvaltot = df_tot[region]
        if group != 'Number of nights in short-term/emergency accommodation':
            ytitle = 'Number of clients'
        else:
            ytitle = 'Number of nights'
    elif view == 'Number of clients per 10,000 people':
        ytitle = 'Number of clients per 10,000 people'
        xvaltot = df_tot['DATE']
        region_pop = f'{region}_POPULATION'
        yvaltot = df_tot[region]/df_tot[region_pop]*10000
    if sex == 'On':
        fig.add_trace(go.Bar(x=xvalfem, y=yvalfem, name='Female'))
        fig.add_trace(go.Bar(x=xvalmal, y=yvalmal, name = 'Male'))
    else:
        fig.add_trace(go.Bar(x=xvaltot, y=yvaltot))
    fig.update_layout(barmode='stack', title=f'WA - {group}', yaxis_title=ytitle)
    st.plotly_chart(fig)
    return    



