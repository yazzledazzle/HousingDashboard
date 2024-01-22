import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def ROGS_sector():
    df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G.csv', encoding='latin-1')
    df['Year'] = df['Year'].astype(str)

    st.markdown(f'Source: <a href="https://www.pc.gov.au/research/ongoing/report-on-government-services/2022/housing-and-homelessness">Report on Government Services 2023, Part G, Sector Overview</a>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    Population = pd.read_csv('DATA/PROCESSED DATA/Population/Population_State_Sex_Age_to_65+.csv')
    #Population filter for All ages, Total, mm=06
    Population['Date'] = pd.to_datetime(Population['Date'], format='%d/%m/%y', dayfirst=True, errors='coerce')

    df = df.rename(columns={'Aust': 'National'})
    regions = ['National', 'WA', 'Vic', 'Qld', 'SA', 'NSW', 'Tas', 'NT', 'ACT']
    #df long = melt on regions, value_name='Value', var_name='Region'
    cols = df.columns.tolist()
    #remove regions from cols
    for region in regions:
        cols.remove(region)
    dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')

    #filter out measure = Households residing in community housing
    df = df[df['Measure'] != 'Households residing in community housing']

    with col1:
        select_measure_sector = st.selectbox('Select measure', df['Measure'].unique())
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Region series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

    df = df[df['Measure'] == select_measure_sector]
    df['Year'] = df['Year'].astype(str)

    if select_measure_sector == "Recurrent expenditure":
        with col2:
            regions_sector = st.multiselect('Select regions', regions, default=regions)
        ytitle = df['Unit'].unique()[0] + ' (' + df['Year_Dollars'].unique()[0] + ')'
        dfRE = df[df['Description3'] == 'Total']
        CRA = dfRE[dfRE['Description2'] == 'Commonwealth Rent Assistance (CRA)']
        NHHA = dfRE[dfRE['Description2'] == 'Total NHHA related expenditure']

        #category bar chart, x=year, y=df[region] for region in regions, color=Description1, group
        fig = go.Figure()
        for region in regions_sector:
            fig.add_trace(go.Bar(x=NHHA['Year'], y=NHHA[region], name=region))
        fig.update_layout(barmode='group', title='NHHA funding', yaxis_title=ytitle)
        #legend below chart
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=1))
        with col1:
            st.plotly_chart(fig)

        fig2 = go.Figure()
        for region in regions_sector:
            fig2.add_trace(go.Bar(x=CRA['Year'], y=CRA[region], name=region))
        fig2.update_layout(barmode='group', title='CRA funding', yaxis_title=ytitle)
        #legend below chart
        fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=1))
        with col2:
            st.plotly_chart(fig2)

    if select_measure_sector == "Low income rental households":
        with col2:
            regions_sector = st.multiselect('Select regions', regions, default=regions)
        dfLIH = df[df['Uncertainty'].isna()]
        select_year_sector = st.selectbox('Select year', dfLIH['Year'].unique())
        dfLIH = dfLIH[dfLIH['Year'] == select_year_sector]
        ytitle1 = "Proportion"
        ytitle2 = "Number"
        dfLIH = dfLIH[dfLIH['Description3'] == 'Paying more than 30% of income on housing costs']
        dfProp = dfLIH[dfLIH['Description4'] == 'Proportion']
        dfNum = dfLIH[dfLIH['Description4'] == 'Number']
        fig = go.Figure()
        fig2 = go.Figure()
        for region in regions_sector:
            fig.add_trace(go.Bar(x=dfProp['Description2'], y=dfProp[region], name=region))
            fig2.add_trace(go.Bar(x=dfNum['Description2'], y=dfNum[region], name=region))
        fig.update_layout(barmode='group', title='Proportion of low income rental households paying more than 30% of income on housing costs', xaxis_title="Remoteness", yaxis_title=ytitle1)
        fig2.update_layout(barmode='group', title='Number of low income rental households paying more than 30% of income on housing costs', xaxis_title="Remoteness", yaxis_title=ytitle2)
        st.plotly_chart(fig)
        st.plotly_chart(fig2)

    if select_measure_sector == "Housing affordability":
        ytitle = df['Description2'].unique()[0]
        charttitle = df['Description1'].unique()[0]
        compare_sector = st.radio('Compare', ['States', 'Years', 'States & years'], horizontal=True)
        if compare_sector == 'States':
            regions_sector = st.multiselect('Select regions', regions, default=regions)
            select_year_sector= st.selectbox('Select year', df['Year'].unique())
            dfHA = df[df['Year'] == select_year_sector]
            fig = go.Figure()
            for region in regions_sector:
                fig.add_trace(go.Bar(x=dfHA['Year'], y=dfHA[region], name=region))
            fig.update_layout(barmode='group', title=charttitle, xaxis_title="Year", yaxis_title=ytitle)
            st.plotly_chart(fig)
        if compare_sector == 'Years':
            regions_sector = st.selectbox('Select region', regions)
            years_sector = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
            fig = go.Figure()
            for year in years_sector:
                dfHA = df[df['Year'] == year]
                fig.add_trace(go.Bar(x=dfHA['Year'], y=dfHA[regions], name=year))
            fig.update_layout(barmode='group', title=charttitle, xaxis_title="Year", yaxis_title=ytitle)
            st.plotly_chart(fig)
        if compare_sector == 'States & years':
            regions_sector = st.multiselect('Select regions', regions, default=regions)
            years_sector = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
            dfHA = df[df['Year'].isin(years_sector)]
            dflong = pd.melt(dfHA, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')
            dflong = dflong[dflong['Region'].isin(regions)]
            #sort dflong by Year ascending
            dflong = dflong.sort_values(by=['Year'], ascending=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(x=[dflong['Region'],dflong['Year']], y=dflong['Value']))
            #add figure inside bar
            fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
            fig.update_layout(barmode='group', title=charttitle, yaxis_title=ytitle)
            st.plotly_chart(fig)
    if select_measure_sector == "Housing composition by tenure type":
        df['Description4'] = df['Description4'].fillna(df['Description3'])
        compare_sector = st.radio('Compare', ['States', 'Years', 'States & years'], horizontal=True)
        df = df[df['Description4'] != 'Total renters']
        df = df[df['Uncertainty'].isna()]
        #sort year ascending
        df = df.sort_values(by=['Year'], ascending=True)
        if compare_sector == 'States':
            regions_sector = st.multiselect('Select regions', regions, default=regions)
            select_year_sector = st.selectbox('Select year', df['Year'].unique())
            df = df[df['Year'] == select_year_sector]   
            fig = go.Figure()
            for region in regions_sector:
                fig.add_trace(go.Bar(x=df['Description4'], y=df[region], name=region))
            fig.update_layout(barmode='group', title='Proportion of renters by tenure type', xaxis_title="Tenure type", yaxis_title="Proportion")
            st.plotly_chart(fig)
        if compare_sector == 'Years':
            regions_sector = st.selectbox('Select region', regions)
            years_sector = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
            df = df[df['Year'].isin(years_sector)]
            #Bar of Year as string category on x, y=df[region] for region, use px
            fig = px.bar(df, x='Year', y=regions, color='Description4', title='Proportion of renters by tenure type', barmode='group', labels={'Year': 'Year', regions: 'Proportion', 'Description4': 'Tenure type'})
            st.plotly_chart(fig)
        if compare_sector == 'States & years':
            regions_sector = st.multiselect('Select regions', regions, default=regions)
            years_sector = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
            df = df[df['Year'].isin(years_sector)]
            dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')
            #for year in years, filter dflong for year, plotly express bar, x=Region, y=Value, color=Region, facet_col=Year
            dflong['Year'] = dflong['Year'].astype(str)
            #dflong Region in regions
            dflong = dflong[dflong['Region'].isin(regions_sector)]
            fig = px.bar(dflong, x='Year', y='Value', color='Description4', facet_col='Region', facet_col_wrap=1, title='Proportion of renters by tenure type', barmode='group', labels={'Region': 'Region', 'Value': '%'})
            #label y value inside bars
            fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
            #legend title Tenure type
            fig.update_layout(legend_title_text='Tenure type')
            #don't show fac
            st.plotly_chart(fig)

    if select_measure_sector == 'Income units receiving CRA':
        #fill blank Special_Need with 'No special need'
        df['Special_Need'] = df['Special_Need'].fillna('No special need')
        filter_for_sector = st.selectbox('Filter for', df['Special_Need'].unique())
        df = df[df['Special_Need'] == filter_for_sector]
        select_sector = st.selectbox('Select', df['Description2'].unique())
        df = df[df['Description2'] == select_sector]
        select_year_sector = st.selectbox('Select year', df['Year'].unique())
        df = df[df['Year'] == select_year_sector]
        regions_sector = st.multiselect('Select regions', regions, default=regions)
        if len(df['Description4'].unique()) > 1:
            filter_sector = st.selectbox('Filter', df['Description3'].unique())
            df = df[df['Description3'] == filter_sector]
        df['Description4'] = df['Description4'].fillna(df['Description3'])
        dfProp = df[df['Unit'] == '%']
        dfNum = df[df['Unit'] == 'no.']
        fig = go.Figure()
        fig2 = go.Figure()
        for region in regions_sector:
            fig.add_trace(go.Bar(x=dfProp['Description4'], y=dfProp[region], name=region))
            fig2.add_trace(go.Bar(x=dfNum['Description4'], y=dfNum[region], name=region))
        st.write(f'Proportion of income units receiving CRA - {filter_for_sector}, {select_sector}, {filter_sector}')
        fig.update_layout(barmode='group',xaxis_title="Category", yaxis_title="Proportion")
        fig2.update_layout(barmode='group', xaxis_title="Category", yaxis_title="Number")
        st.plotly_chart(fig)
        st.write(f'Number of income units receiving CRA - {filter_for_sector}, {select_sector}, {filter_sector}')
        st.plotly_chart(fig2)
    return

                

def ROGS_housing():
    st.markdown(f'Source: <a href="https://www.pc.gov.au/ongoing/report-on-government-services/2023/housing-and-homelessness/housing">Report on Government Services 2023, Part G, Section 18 - Housing</a>', unsafe_allow_html=True)

    rogshousing = pd.read_csv("DATA/SOURCE DATA/ROGS and SHS/ROGS G18.csv", encoding='latin-1')

    #remove Measure values Descriptive data, Survey response rates, Self-reported benefits of living in social housing - Public housing, Self-reported benefits of living in social housing - SOMIH, Self-reported benefits of living in social housing - Community housing
    rogshousing = rogshousing[rogshousing['Measure'] != 'Descriptive data']
    rogshousing = rogshousing[rogshousing['Measure'] != 'Survey response rates']
    rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - Public housing']
    rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - SOMIH']
    rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - Community housing']



    col1, col2 = st.columns(2)
    with col1: 
        measure = st.selectbox('Measure', rogshousing['Measure'].unique())
        filtered_data=rogshousing[rogshousing['Measure']==measure]
        if measure == 'Recurrent expenditure':
            filtered_data = filtered_data[filtered_data['Housing_Type'] != 'Community housing']
            filtered_data = filtered_data[filtered_data['Housing_Type'].notna()]
            filtered_data = filtered_data[filtered_data['Housing_Type'] != 'Indigenous community housing']

    with col1:
        housing_type = st.selectbox('Housing type', filtered_data['Housing_Type'].unique())
        filtered_data=filtered_data[filtered_data['Housing_Type']==housing_type]
    with col2:
        desc1 = st.selectbox('Description1', filtered_data['Description1'].unique())
        filtered_data=filtered_data[filtered_data['Description1']==desc1]
        desc2 = st.selectbox('Description2', filtered_data['Description2'].unique())
        filtered_data=filtered_data[filtered_data['Description2']==desc2]
    with col1:
        if len(filtered_data['Description3'].unique()) > 1:
            desc3 = st.selectbox('Description3', filtered_data['Description3'].unique())
            filtered_data=filtered_data[filtered_data['Description3']==desc3]
    with col2:
        if len(filtered_data['Description4'].unique()) > 1:
            desc4 = st.selectbox('Description4', filtered_data['Description4'].unique())
            filtered_data=filtered_data[filtered_data['Description4']==desc4]
    with col1:
        if len(filtered_data['Description5'].unique()) > 1:
            desc5 = st.selectbox('Description5', filtered_data['Description5'].unique())
            filtered_data=filtered_data[filtered_data['Description5']==desc5]
    with col2:
        if len(filtered_data['Description6'].unique()) > 1:
            desc6 = st.selectbox('Description6', filtered_data['Description6'].unique())
            filtered_data=filtered_data[filtered_data['Description6']==desc6]
    with col1:
        chart_type = st.radio('Chart type', ['Line chart', 'Bar chart'])
    with col2:
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

    if len(filtered_data['Total'].unique()) > 1:
        regions = ['Total', 'WA','NSW', 'Vic', 'Qld', 'WA', 'SA','Tas', 'ACT', 'NT']
    else:
        regions = ['Aust', 'WA', 'NSW', 'Vic', 'Qld', 'SA','Tas', 'ACT', 'NT']



    fig=go.Figure()

    if chart_type == 'Line chart':
        for region in regions:
            fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data[region], name=region, mode='lines+markers'))
        fig.update_layout(title_text=f'{measure} - {desc1} {desc2}', yaxis=dict(title=filtered_data['Unit'].unique()[0]), xaxis=dict(title='Year'))

    else:
        for region in regions:
            fig.add_trace(go.Bar(x=filtered_data['Year'], y=filtered_data[region], name=region))
        fig.update_layout(title_text=f'{measure} - {desc1} {desc2}', yaxis=dict(title=filtered_data['Unit'].unique()[0]), xaxis=dict(title='Year'), barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    return

def ROGS_homelessness():
    st.markdown(f'Source: <a href="https://www.pc.gov.au/ongoing/report-on-government-services/2023/housing-and-homelessness/homelessness-services">Report on Government Services 2023, Part G, Section 19 - Homelessness Services</a>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G19.csv', encoding='latin-1')
    df['Year'] = df['Year'].astype(str)

    df = df.rename(columns={'Aust': 'National'})
    regions = ['National', 'WA', 'Vic', 'Qld', 'SA', 'NSW', 'Tas', 'NT', 'ACT']
    #df long = melt on regions, value_name='Value', var_name='Region'
    cols = df.columns.tolist()
    #remove regions from cols
    for region in regions:
        cols.remove(region)
    dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')

    #filter out measure = Rate of homeless people, Composition of support provided, Access of selected equity groups, Addressing client needs, Achievement of employment; education and/or training on exit, Achievement of income on exit,Clients at risk of homelessness who avoided homelessness,Support periods in which clients at risk of homelessness avoided homelessness,Achievement of independent housing on exit,Clients who return to homelessness after achieving housing, Clients who experience persistent homelessness
    df = df[df['Measure'] != 'Rate of homeless people']
    df = df[df['Measure'] != 'Composition of support provided']
    df = df[df['Measure'] != 'Access of selected equity groups']
    df = df[df['Measure'] != 'Addressing client needs']
    df = df[df['Measure'] != 'Achievement of employment; education and/or training on exit']
    df = df[df['Measure'] != 'Achievement of income on exit']
    df = df[df['Measure'] != 'Clients at risk of homelessness who avoided homelessness']
    df = df[df['Measure'] != 'Support periods in which clients at risk of homelessness avoided homelessness']
    df = df[df['Measure'] != 'Achievement of independent housing on exit']
    df = df[df['Measure'] != 'Clients who return to homelessness after achieving housing']
    df = df[df['Measure'] != 'Clients who experience persistent homelessness']


    with col1:
        select_measure = st.selectbox('Select measure', df['Measure'].unique())

    df = df[df['Measure'] == select_measure]
    df['Year'] = df['Year'].astype(str)

    if select_measure == "Recurrent expenditure":
        
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Region series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)
        ytitle = df['Unit'].unique()[0] + ' (' + df['Year_Dollars'].unique()[0] + ')'
        with col2:
            showas = st.radio('Show as', ['Total', 'Per person in population'], index=0, horizontal=True)
        if showas == 'Total':
            dfRE = df[df['Description2'] == 'Total recurrent real expenditure']
            charttitle = 'Total recurrent real expenditure'
        if showas == 'Per person in population':
            dfRE = df[df['Description2'] == 'Real expenditure per person in the residential population']
            charttitle = 'Real expenditure per person in the residential population'
        fig = go.Figure()
        for region in regions:
            fig.add_trace(go.Bar(x=dfRE['Year'], y=dfRE[region], name=region))
        fig.update_layout(barmode='group', title='Recurrent expenditure - homelessness services', xaxis_title="Year", yaxis_title=ytitle)
        st.plotly_chart(fig)


    if select_measure == "Unmet need":
        filter1 = st.selectbox('Select filter', ['Accommodation services', 'Services other than accommodation'], index=0, key='filter1')
        
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Region series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)
        if filter1 == 'Accommodation services':
            df_fig2 = df[df['Description1'] == 'Average daily unassisted requests']
            df_fig2 = df_fig2.sort_values(by=['Year'], ascending=True)
            df_fig2 = df_fig2[df_fig2['Description2'] == 'Accommodation services']
            fig2 = go.Figure()
            for region in regions:
                fig2.add_trace(go.Bar(x=df_fig2['Year'], y=df_fig2[region], name=region))
            fig2.update_layout(barmode='group', title='Average daily unassisted requests', xaxis_title="Year", yaxis_title='Number')
            st.plotly_chart(fig2)
            df_fig1 = df[df['Description1'] == 'Accommodation services']
            #sort Year ascending
            df_fig1 = df_fig1.sort_values(by=['Year'], ascending=True)
            for Desc2 in df_fig1['Description2'].unique().tolist():
                fig1 = go.Figure()
                df_fig1_fil = df_fig1[df_fig1['Description2'] == Desc2]
                for region in regions:
                    fig1.add_trace(go.Bar(x=df_fig1_fil['Year'], y=df_fig1_fil[region], name=region))
                fig1.update_layout(barmode='group', title=Desc2, xaxis_title="Year", yaxis_title='Number')
                st.plotly_chart(fig1)
        if filter1 == 'Services other than accommodation':
            df_fig2 = df[df['Description1'] == 'Average daily unassisted requests']
            df_fig2 = df_fig2.sort_values(by=['Year'], ascending=True)
            df_fig2 = df_fig2[df_fig2['Description2'] == 'Services other than accommodation']
            fig2 = go.Figure()
            for region in regions:
                fig2.add_trace(go.Bar(x=df_fig2['Year'], y=df_fig2[region], name=region))
            fig2.update_layout(barmode='group', title='Average daily unassisted requests', xaxis_title="Year", yaxis_title='Number')
            st.plotly_chart(fig2)
            df_fig1 = df[df['Description1'] == 'Services other than accommodation']
            #sort Year ascending
            df_fig1 = df_fig1.sort_values(by=['Year'], ascending=True)
            for Desc2 in df_fig1['Description2'].unique().tolist():
                fig1 = go.Figure()
                df_fig1_fil = df_fig1[df_fig1['Description2'] == Desc2]
                for region in regions:
                    fig1.add_trace(go.Bar(x=df_fig1_fil['Year'], y=df_fig1_fil[region], name=region))
                fig1.update_layout(barmode='group', title=Desc2, xaxis_title="Year", yaxis_title='Number')
                st.plotly_chart(fig1)
    return
