import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def home():
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
    return

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

def waitlist_latest():

  Waitlist_trend_latest = pd.read_csv('DATA/PROCESSED DATA/PUBLIC HOUSING/Waitlist_trend_latest.csv')

  class WaitlistUpdate:
      def __init__(self, Date, Category, Subcategory, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value, FontColor):
          self.Date = Date
          self.Category = Category
          self.Subcategory = Subcategory
          self.Metric = Metric
          self.MetricDetail = MetricDetail
          self.MetricAs = MetricAs
          self.MetricCalc = MetricCalc
          self.MetricCalcAs = MetricCalcAs
          self.Estimate = Estimate
          self.Value = Value
          self.FontColor = FontColor

  waitlist_updates = []

  for index, row in Waitlist_trend_latest.iterrows():
      update = WaitlistUpdate(
          Date = row['Date'],
          Category = row['Description1'],
          Subcategory = row['Description2'],
          Metric = row['Description3'],
          MetricDetail = row['Description4'],
          MetricAs = row['Description5'],
          MetricCalc = row['Description6'],
          MetricCalcAs = row['Description7'],
          Estimate = row['Estimate'],
          Value = row['Value'],
          FontColor = "red" if row['Value'] > 0 else "green"
      )
      waitlist_updates.append(update)

  TotalApplications, TotalIndividuals, PriorityApplications, PriorityIndividuals, NonpriorityApplications, NonpriorityIndividuals, ProportionPriorityApplications, ProportionPriorityIndividuals, AveragePersonsTotal, AveragePersonsPriority, AveragePersonsNonpriority = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

  categories = [(TotalApplications, 'Total', 'Applications'), 
                (TotalIndividuals, 'Total', 'Individuals'), 
                (PriorityApplications, 'Priority', 'Applications'), 
                (PriorityIndividuals, 'Priority', 'Individuals'),
                  (NonpriorityApplications, 'Nonpriority', 'Applications'),
                  (NonpriorityIndividuals, 'Nonpriority', 'Individuals'),
                (ProportionPriorityApplications, 'Proportion Priority', 'Applications'),
                (ProportionPriorityIndividuals, 'Proportion Priority', 'Individuals'),
                  (AveragePersonsTotal, 'Average Number Of Individuals Per Application', 'Total'),
                  (AveragePersonsPriority, 'Average Number Of Individuals Per Application', 'Priority'),
                  (AveragePersonsNonpriority, 'Average Number Of Individuals Per Application', 'Nonpriority')
                ]
      
  for category, cat1, cat2 in categories:
          category['Date'] = [x.Date for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2]
          category['Date'] = max(category['Date'])
          category['Value'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Prior month change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
          category['Prior month change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior year change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Prior year change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
          category['Prior year change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc =='-']
          category['Rolling average prior month difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior month difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
          category['Rolling average prior month difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior year difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior year difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
          category['Rolling average prior year difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          if cat2 == 'Individuals' and cat1 != 'Proportion Priority':
              category['per 10 000'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
              category['per 10 000 prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
              category['per 10 000 prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['per 10 000 rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['percentage of population'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
              category['percentage of population prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
              category['percentage of population prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
              category['percentage of population prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              
  #latest date is max of TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'], taken as datetime from yyyy-mm-dd, converted to dd mmmm yyyy
  latest_date = max(TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'])
  latest_date = pd.to_datetime(latest_date)
  latest_date = latest_date.strftime('%d %B %Y')

  Waitlist_trend_latest = pd.read_csv('DATA/PROCESSED DATA/PUBLIC HOUSING/Waitlist_trend_latest.csv')

  class WaitlistUpdate:
      def __init__(self, Date, Category, Subcategory, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value, FontColor):
          self.Date = Date
          self.Category = Category
          self.Subcategory = Subcategory
          self.Metric = Metric
          self.MetricDetail = MetricDetail
          self.MetricAs = MetricAs
          self.MetricCalc = MetricCalc
          self.MetricCalcAs = MetricCalcAs
          self.Estimate = Estimate
          self.Value = Value
          self.FontColor = FontColor

  waitlist_updates = []

  for index, row in Waitlist_trend_latest.iterrows():
      update = WaitlistUpdate(
          Date = row['Date'],
          Category = row['Description1'],
          Subcategory = row['Description2'],
          Metric = row['Description3'],
          MetricDetail = row['Description4'],
          MetricAs = row['Description5'],
          MetricCalc = row['Description6'],
          MetricCalcAs = row['Description7'],
          Estimate = row['Estimate'],
          Value = row['Value'],
          FontColor = "red" if row['Value'] > 0 else "green"
      )
      waitlist_updates.append(update)

  TotalApplications, TotalIndividuals, PriorityApplications, PriorityIndividuals, NonpriorityApplications, NonpriorityIndividuals, ProportionPriorityApplications, ProportionPriorityIndividuals, AveragePersonsTotal, AveragePersonsPriority, AveragePersonsNonpriority = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

  categories = [(TotalApplications, 'Total', 'Applications'), 
              (TotalIndividuals, 'Total', 'Individuals'), 
              (PriorityApplications, 'Priority', 'Applications'), 
              (PriorityIndividuals, 'Priority', 'Individuals'),
                  (NonpriorityApplications, 'Nonpriority', 'Applications'),
                  (NonpriorityIndividuals, 'Nonpriority', 'Individuals'),
              (ProportionPriorityApplications, 'Proportion Priority', 'Applications'),
              (ProportionPriorityIndividuals, 'Proportion Priority', 'Individuals'),
                  (AveragePersonsTotal, 'Average Number Of Individuals Per Application', 'Total'),
                  (AveragePersonsPriority, 'Average Number Of Individuals Per Application', 'Priority'),
                  (AveragePersonsNonpriority, 'Average Number Of Individuals Per Application', 'Nonpriority')
              ]
      
  for category, cat1, cat2 in categories:
          category['Date'] = [x.Date for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2]
          category['Date'] = max(category['Date'])
          category['Value'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior month change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Prior month change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
          category['Prior month change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Prior year change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Prior year change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
          category['Prior year change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
          category['Rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
          category['Rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc =='-']
          category['Rolling average prior month difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior month difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
          category['Rolling average prior month difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior year difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          category['Rolling average prior year difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
          category['Rolling average prior year difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
          if cat2 == 'Individuals' and cat1 != 'Proportion Priority':
              category['per 10 000'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
              category['per 10 000 prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['per 10 000 prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
              category['per 10 000 prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['per 10 000 rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
              category['per 10 000 rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
              category['percentage of population'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
              category['percentage of population prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
              category['percentage of population prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              category['percentage of population prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
              category['percentage of population prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
              
  #latest date is max of TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'], taken as datetime from yyyy-mm-dd, converted to dd mmmm yyyy
  latest_date = max(TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'])
  latest_date = pd.to_datetime(latest_date)
  latest_date = latest_date.strftime('%d %B %Y')

  st.markdown(f'### As at ' + latest_date)
  #two columns, heading2 on left  = Applications, heading2 on right = Individuals
  st.markdown(f'''
              <style>
              .custom-table {{
          width: 80%;
          border-collapse: separate;
      }}
      .custom-table th, .custom-table td {{
          font-family: Tahoma;
          text-align: center;
          border: none;
      }}
      .custom-table th {{
          background-color: transparent;
          border-bottom: none;
      }}
      .header-row {{
          font-weight: bold;
          background-color: transparent;
          border-bottom: 1px solid #d3d3d3;
      }}
      .data-row {{
          height: 1.2cm;
      }}
      .data-cell-total-count {{
          border-right: 3px dotted #d3d3d3;
          background-color: #ffff75;
          font-weight: bold;
          font-size: 18px;
      }}
              
      .data-cell-total {{
          border-right: 3px dotted #d3d3d3;
          background-color: transparent;
      }}
              
      .data-cell-nonpriority {{
          background-color: #f0f0f0;
      }}
      
      .data-cell-priority {{
          background-color: #f7e7e6;
      }}
              
      .data-cell-proportion {{
          background-color: #f7f5e6;
          font-style: italic;
      }}

              
      .pm-ta {{
              color: {TotalApplications["Prior month font color"][0]};
              }}
      .pm-pa {{
              color: {PriorityApplications["Prior month font color"][0]};
              }}
      .pm-npa {{
              color: {NonpriorityApplications["Prior month font color"][0]};
              }}

      .pm-ti {{
              color: {TotalIndividuals["Prior month font color"][0]};
              }}
      .pm-pi {{
              color: {PriorityIndividuals["Prior month font color"][0]};
              }}

      .pm-npi {{
              color: {NonpriorityIndividuals["Prior month font color"][0]};
              }}

      .pm-ppa {{
              color: {ProportionPriorityApplications["Prior month font color"][0]};
              }}

      .pm-ppi {{
              color: {ProportionPriorityIndividuals["Prior month font color"][0]};
              }}

      .pm-t10k {{
              color: {TotalIndividuals["per 10 000 prior month font color"][0]};
              }}

      .pm-p10k {{
              color: {PriorityIndividuals["per 10 000 prior month font color"][0]};
              }}

      .pm-np10k {{
              color: {NonpriorityIndividuals["per 10 000 prior month font color"][0]};
              }}

      .pm-tpop {{
              color: {TotalIndividuals["percentage of population prior month font color"][0]};
              }}

      .pm-ppop {{
              color: {PriorityIndividuals["percentage of population prior month font color"][0]};
              }}

      .pm-npop {{
              color: {NonpriorityIndividuals["percentage of population prior month font color"][0]};
              }}

      .pm-tavgppa {{
              color: {AveragePersonsTotal["Prior month font color"][0]};
              }}

      .pm-pavgppa {{
              color: {AveragePersonsPriority["Prior month font color"][0]};
              }}

      .pm-npavgppa {{
              color: {AveragePersonsNonpriority["Prior month font color"][0]};
              }}

      .py-ta {{
              color: {TotalApplications["Prior year font color"][0]};
              }}

      .py-pa {{
              color: {PriorityApplications["Prior year font color"][0]};
              }}

      .py-npa {{
              color: {NonpriorityApplications["Prior year font color"][0]};
              }}

      .py-ti {{
              color: {TotalIndividuals["Prior year font color"][0]};
              }}

      .py-pi {{
              color: {PriorityIndividuals["Prior year font color"][0]};
              }}

      .py-npi {{
              color: {NonpriorityIndividuals["Prior year font color"][0]};
              }}

      .py-ppa {{
          color: {ProportionPriorityApplications["Prior year font color"][0]};
              }}

      .py-ppi {{
          color: {ProportionPriorityIndividuals["Prior year font color"][0]};
                  }}

      .py-t10k {{
                  color: {TotalIndividuals["per 10 000 prior year font color"][0]};
                  }}

      .py-p10k {{
          color: {PriorityIndividuals["per 10 000 prior year font color"][0]};
          }}

      .py-np10k {{
      color: {NonpriorityIndividuals["per 10 000 prior year font color"][0]};
      }}

      .py-tpop {{
      color: {TotalIndividuals["percentage of population prior year font color"][0]};
      }}

      .py-ppop {{
      color: {PriorityIndividuals["percentage of population prior year font color"][0]};
      }}

      .py-npop {{
      color: {NonpriorityIndividuals["percentage of population prior year font color"][0]};
      }}

      .py-tavgppa {{
      color: {AveragePersonsTotal["Prior year font color"][0]};
      }}

      .py-pavgppa {{
      color: {AveragePersonsPriority["Prior year font color"][0]};
      }}

      .ra-ta {{
      color: {TotalApplications["Rolling average difference font color"][0]};
      }}

      .ra-pa {{
      color: {PriorityApplications["Rolling average difference font color"][0]};
      }}

      .ra-pi {{
      color: {PriorityIndividuals["Rolling average difference font color"][0]};
      }}

      .ra-ti {{
      color: {TotalIndividuals["Rolling average difference font color"][0]};
      }}

      .ra-pm-ta {{
      color: {TotalApplications["Rolling average prior month difference font color"][0]};
      }}

      .ra-pm-pa {{
      color: {PriorityApplications["Rolling average prior month difference font color"][0]};
      }}

      .ra-pm-pi {{
      color: {PriorityIndividuals["Rolling average prior month difference font color"][0]};
      }}

      .ra-pm-ti {{
      color: {TotalIndividuals["Rolling average prior month difference font color"][0]};
      }}

      
      .data-cell-total-count, .data-cell-priority, data-cell-nonpriority, .data-cell-total, .pm-ta, .pm-pa, .pm-npa, .pm-ti, .pm-pi, .pm-npi, .pm-tp, .pm-ip, .pm-tpp, .pm-pp, .pm-npp, .pm-tpop, .pm-ipop, .pm-npop, .pm-tavgppa, .pm-pavgppa, .pm-npavgppa, .py-ta, .py-pa, .py-npa, .py-ti, .py-pi, .py-npi, .py-tp, .py-ip, .py-tpp, .py-pp, .py-npp, .py-tpop, .py-ipop, .py-npop, .py-tavgppa, .py-pavgppa, .py-npavgppa, .ra-ta, .ra-pa, .ra-pi, .ra-ti, .ra-pm-ta, .ra-pm-pa, .ra-pm-pi, .ra-pm-ti {{
          height: 0.8cm;
          width: 0.8cm;
      }}

      .header-cell-total-count {{
          border-right: 3px dotted #d3d3d3;
          background-color: #ffff75;
          font-weight: bold;
          font-size: 18px;
      }}
              
      .header-cell-total {{
          border-right: 3px dotted #d3d3d3;
          background-color: transparent;
      }}
      
      .header-cell-priority {{
          background-color: #f7e7e6;
      }}
      
      .header-cell-proportion {{
          background-color: #f7f5e6;
              font-style: italic;
      }}
              
      .header-cell-nonpriority {{
          background-color: #f0f0f0;
      }}
              
      .header-cell-total, .header-cell-priority, .header-cell-nonpriority, .header-cell-proportion {{
          height: 1cm;
          width: 0.8cm;
          font-weight: bold;
          font-size: 14px;
      }}
      
      .header-applications {{
          background-color: #add8e6;
          font-weight: bold;
          font-size: 18px;
      }}

      .header-percent{{
          background-color: #b3b3f5;
          font-style: italic;
          font-weight: bold;
          font-size: 18px;
      }}

      .header-count {{
          background-color: #eeb3f5;
          font-style: italic;
          font-weight: bold;
          font-size: 18px;
      }}
              
      .header-persons-per-application {{
          background-color: #cafaf8;
          font-style: italic;
          font-size: 14px;
      }}
              
      .header-individuals {{
          background-color: #90ee90;
          font-weight: bold;
          font-size: 18px;
      }}
              
      .header-individuals-per-10k {{
          background-color: #f0e68c;
          font-style: italic;
          font-size: 14px;
      }}
      
      .header-individuals-percentage {{
          background-color: #ffd4b3;
          font-style: italic;
          font-size: 14px;
      }}
      
      .spacer-column {{
          width: 0.1cm; 
      }}
              </style>
  <table class="custom-table">
      <tr>
          <td colspan="8" class="header-applications">APPLICATIONS</td>
          <td class="spacer-column"></td>
          <td colspan="12" class="header-individuals">INDIVIDUALS</td>
      </tr>
      <tr>
          <td colspan="4" class="header-cell-total"></td>
          <td class="spacer-column"></td>
          <td colspan="3" class="header-persons-per-application">Avg. persons per application</td>
          <td class="spacer-column"></td>
          <td colspan="4" class ="header-cell-total"></td>
          <td class="spacer-column"></td>
          <td colspan="3" class="header-individuals-per-10k">Per 10,000 people</td>
          <td class="spacer-column"></td>
          <td colspan="3" class="header-individuals-percentage">As percent of population</td>
          </tr>
      <tr class="header-row">
          <td class="header-cell-total-count">TOTAL</td>
          <td class="header-cell-priority">Priority</td>
          <td class="header-cell-nonpriority">Non-priority</td>
          <td class="header-cell-proportion">% priority</td>
          <td class="spacer-column"></td>
          <td class="header-cell-total">Total</td>
          <td class="header-cell-priority">Priority</td>
          <td class="header-cell-nonpriority">Non-priority</td>
          <td class="spacer-column"></td>
          <td class="header-cell-total-count">TOTAL</td>
          <td class="header-cell-priority">Priority</td>
          <td class="header-cell-nonpriority">Non-priority</td>
          <td class="header-cell-proportion">% priority</td>
          <td class="spacer-column"></td>
          <td class="header-cell-total">Total</td>
          <td class="header-cell-priority">Priority</td>
          <td class="header-cell-nonpriority">Non-priority</td>
          <td class="spacer-column"></td>
          <td class="header-cell-total">Total</td>
          <td class="header-cell-priority">Priority</td>
          <td class="header-cell-nonpriority">Non-priority</td>
      </tr>
      <tr class="data-row">
          <td class="data-cell-total-count">{TotalApplications["Value"][0]:,.0f}</td>
          <td class="data-cell-priority">{PriorityApplications["Value"][0]:,.0f}</td>
          <td class="data-cell-nonpriority">{NonpriorityApplications["Value"][0]:,.0f}</td>
          <td class="data-cell-proportion">{ProportionPriorityApplications["Value"][0]:,.1f}%</td>
          <td class="spacer-column"></td>
          <td class="data-cell-total">{AveragePersonsTotal["Value"][0]:,.1f}</td>
          <td class="data-cell-priority">{AveragePersonsPriority["Value"][0]:,.1f}</td>
          <td class="data-cell-nonpriority">{AveragePersonsNonpriority["Value"][0]:,.1f}</td>
          <td class="spacer-column"></td>
          <td class="data-cell-total-count">{TotalIndividuals["Value"][0]:,.0f}</td>
          <td class="data-cell-priority">{PriorityIndividuals["Value"][0]:,.0f}</td>
          <td class="data-cell-nonpriority">{NonpriorityIndividuals["Value"][0]:,.0f}</td>
          <td class="data-cell-proportion">{ProportionPriorityIndividuals["Value"][0]:,.1f}%</td>
          <td class="spacer-column"></td>
          <td class="data-cell-total">{TotalIndividuals["per 10 000"][0]:,.0f}</td>
          <td class="data-cell-priority">{PriorityIndividuals["per 10 000"][0]:,.0f}</td>
          <td class="data-cell-nonpriority">{NonpriorityIndividuals["per 10 000"][0]:,.0f}</td>
          <td class="spacer-column"></td>
          <td class="data-cell-total">{TotalIndividuals["percentage of population"][0]:,.2f}%</td>
          <td class="data-cell-priority">{PriorityIndividuals["percentage of population"][0]:,.2f}%</td>
          <td class="data-cell-nonpriority">{NonpriorityIndividuals["percentage of population"][0]:,.2f}%</td>
      </tr>
  </table>
  ''', unsafe_allow_html=True)

  st.markdown('</br>', unsafe_allow_html=True)
  st.markdown(f'**Changes from prior month**')
  st.markdown(f'''
  <table class="custom-table">
          <tr class="header-row">
              <tr>
          <td colspan="7" class="header-percent">%</td>
          <td class="spacer-column"></td>
          <td colspan="7" class="header-count">NUMBER</td>
      </tr>
      <tr class="header-row">
              <tr>
              <td colspan="3", class="header-applications">APPLICATIONS</td>
              <td class="spacer-column"></td>
              <td colspan="3", class="header-individuals">INDIVIDUALS</td>
              <td class="spacer-column"></td>
  <td colspan="3", class="header-applications">APPLICATIONS</td>
              <td class="spacer-column"></td>
              <td colspan="3", class="header-individuals">INDIVIDUALS</td>
              </tr>
              <tr>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
      <tr class="data-row">
                  <td class= "pm-ta">{TotalApplications["Prior month %"][0]:,.2f}%</td>
          <td class="pm-pa">{PriorityApplications["Prior month %"][0]:,.2f}%</td>
          <td class="pm-npa">{NonpriorityApplications["Prior month %"][0]:,.2f}%</td>
          <td class="spacer-column"></td>
          <td class="pm-ti">{TotalIndividuals["Prior month %"][0]:,.2f}%</td>
          <td class="pm-pi">{PriorityIndividuals["Prior month %"][0]:,.2f}%</td>
          <td class="pm-npi">{NonpriorityIndividuals["Prior month %"][0]:,.2f}%</td>
          <td class="spacer-column"></td>
              <td class= "pm-ta">{TotalApplications["Prior month"][0]:,.0f}</td>
          <td class="pm-pa">{PriorityApplications["Prior month"][0]:,.0f}</td>
          <td class="pm-npa">{NonpriorityApplications["Prior month"][0]:,.0f}</td>
          <td class="spacer-column"></td>
          <td class="pm-ti">{TotalIndividuals["Prior month"][0]:,.0f}</td>
          <td class="pm-pi">{PriorityIndividuals["Prior month"][0]:,.0f}</td>
          <td class="pm-npi">{NonpriorityIndividuals["Prior month"][0]:,.0f}</td>
  ''', unsafe_allow_html=True)
  #add title and table for prior year
  st.markdown('</br>', unsafe_allow_html=True)
  st.markdown(f'**Changes from prior year**')
  st.markdown(f'''
      <table class="custom-table">
          <tr class="header-row">
              <tr>
          <td colspan="7" class="header-percent">%</td>
          <td class="spacer-column"></td>
          <td colspan="7" class="header-count">NUMBER</td>
      </tr>
      <tr class="header-row">
              <tr>
              <td colspan="3", class="header-applications">APPLICATIONS</td>
              <td class="spacer-column"></td>
              <td colspan="3", class="header-individuals">INDIVIDUALS</td>
              <td class="spacer-column"></td>
  <td colspan="3", class="header-applications">APPLICATIONS</td>
              <td class="spacer-column"></td>
              <td colspan="3", class="header-individuals">INDIVIDUALS</td>
              </tr>
              <tr>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
              <td class="spacer-column"></td>
              <td class="header-cell-total-count">TOTAL</td>
              <td class="header-cell-priority">Priority</td>
              <td class="header-cell-nonpriority">Non-priority</td>
      <tr class="data-row">
                  <td class= "py-ta">{TotalApplications["Prior year %"][0]:,.2f}%</td>
          <td class="py-pa">{PriorityApplications["Prior year %"][0]:,.2f}%</td>
          <td class="py-npa">{NonpriorityApplications["Prior year %"][0]:,.2f}%</td>
          <td class="spacer-column"></td>
          <td class="py-ti">{TotalIndividuals["Prior year %"][0]:,.2f}%</td>
          <td class="py-pi">{PriorityIndividuals["Prior year %"][0]:,.2f}%</td>
          <td class="py-npi">{NonpriorityIndividuals["Prior year %"][0]:,.2f}%</td>
          <td class="spacer-column"></td>
              <td class= "py-ta">{TotalApplications["Prior year"][0]:,.0f}</td>
          <td class="py-pa">{PriorityApplications["Prior year"][0]:,.0f}</td>
          <td class="py-npa">{NonpriorityApplications["Prior year"][0]:,.0f}</td>
          <td class="spacer-column"></td>
          <td class="py-ti">{TotalIndividuals["Prior year"][0]:,.0f}</td>
          <td class="py-pi">{PriorityIndividuals["Prior year"][0]:,.0f}</td>
          <td class="py-npi">{NonpriorityIndividuals["Prior year"][0]:,.0f}</td>
  ''', unsafe_allow_html=True)
  return

def waitlist_trendcharts():
    data = pd.read_csv('DATA/PROCESSED DATA/PUBLIC HOUSING/Waitlist_trend_long.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    latest_date = data['Date'].max()
    latest_date = pd.to_datetime(latest_date, format='%Y-%m-%d').strftime('%B %Y')
    st.markdown(f'Source: <a href="https://www.parliament.wa.gov.au/Parliament/Pquest.nsf/(SearchResultsAllDesc)?SearchView&Query=(Housing%20waitlist)&Start=1&SearchOrder=4&SearchMax=1000">Parliamentary questions - last updated {latest_date} </a>', unsafe_allow_html=True)
    class WaitlistTrend:
        def __init__(self, Date, Category, Subcategory, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value, FontColor):
            self.Date = Date
            self.Category = Category
            self.Subcategory = Subcategory
            self.Metric = Metric
            self.MetricDetail = MetricDetail
            self.MetricAs = MetricAs
            self.MetricCalc = MetricCalc
            self.MetricCalcAs = MetricCalcAs
            self.Estimate = Estimate
            self.Value = Value
            self.FontColor = FontColor

    waitlist_trend = [] 
    for index, row in data.iterrows():
        trend = WaitlistTrend(
            Date = row['Date'],
            Category = row['Description1'],
            Subcategory = row['Description2'],
            Metric = row['Description3'],
            MetricDetail = row['Description4'],
            MetricAs = row['Description5'],
            MetricCalc = row['Description6'],
            MetricCalcAs = row['Description7'],
            Estimate = row['Estimate'],
            Value = row['Value'],
            FontColor = "red" if row['Value'] > 0 else "green"

        )
        waitlist_trend.append(trend)   
    col1, col2, col3 = st.columns(3)

    with col1:
        select = st.selectbox('Category', ['Applications', 'Individuals'])

    with col2:
        if select == 'Applications':
            axis2 = st.selectbox('Second axis', ['Proportion of Waitlist that is priority', 'Average Number Of Individuals Per Application', 'None'])
        else:
            axis2 = st.selectbox('Second axis', ['per 10 000', 'Percentage of population', 'None'])

    with col3:
        st.markdown(f'</br>', unsafe_allow_html=True)
        Show_Rolling = col3.checkbox('Include 12 month rolling average line')
        graph_type = col3.radio('Display', ['Priority & total', 'Priority & non-priority'], horizontal=True)

    dates = [x.Date for x in waitlist_trend]
    dates = pd.DataFrame(columns=['Date'], data=dates)
    #set to datetime
    dates['Date'] = pd.to_datetime(dates['Date'])
    max_date = dates['Date'].max()
    if graph_type == 'Priority & non-priority':
        min_date = '2021-09-30'
        min_date = pd.to_datetime(min_date)
    else:
        min_date = dates['Date'].min()
    daterange = dates[(dates['Date'] >= min_date) & (dates['Date'] <= max_date)]
    #sort and drop duplicates
    daterange = daterange.sort_values(by=['Date'], ascending=True)
    daterange = daterange.drop_duplicates(subset=['Date'], keep='first')

    st.markdown("**Select date range:**")
    select_date_slider= st.select_slider('', options=daterange, value=(min_date, max_date), format_func=lambda x: x.strftime('%b %y'))
    startgraph, endgraph = list(select_date_slider)[0], list(select_date_slider)[1]
    #filter data based on date range
    waitlist_trend = [x for x in waitlist_trend if x.Date >= startgraph and x.Date <= endgraph]

    waitlist_totalapp = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_totalapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_totalapp])
    waitlist_priorityapp = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_priorityapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_priorityapp])
    waitlist_nonpriorityapp = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_nonpriorityapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_nonpriorityapp])
    waitlist_totalind = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_totalind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_totalind])
    waitlist_priorityind = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_priorityind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_priorityind])
    waitlist_nonpriorityind = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_nonpriorityind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_nonpriorityind])
    waitlist_proportionpriority = [x for x in waitlist_trend if x.Category == 'Proportion Priority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_proportionpriority = pd.DataFrame.from_records([s.__dict__ for s in waitlist_proportionpriority])
    waitlist_averageperapptot = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Total' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_averageperapptot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperapptot])
    waitlist_averageperapppri = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Priority' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_averageperapppri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperapppri])
    waitlist_averageperappnon = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Nonpriority' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    waitlist_averageperappnon = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperappnon])
    waitlist_per10000tot = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
    waitlist_per10000tot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000tot])
    waitlist_per10000pri = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
    waitlist_per10000pri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000pri])
    waitlist_per10000non = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
    waitlist_per10000non = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000non])
    waitlist_percentagetot = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
    waitlist_percentagetot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagetot])
    waitlist_percentagepri = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
    waitlist_percentagepri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagepri])
    waitlist_percentagenon = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
    waitlist_percentagenon = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagenon])
    rolling_avgtotapp = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgtotapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgtotapp])
    rolling_avgpriapp = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgpriapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgpriapp])
    rolling_avgnonapp = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgnonapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgnonapp])
    rolling_avgtotind = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgtotind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgtotind])
    rolling_avgpriind = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgpriind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgpriind])
    rolling_avgnonind = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
    rolling_avgnonind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgnonind])


    fig = go.Figure()
    if select == 'Applications':
        if graph_type == 'Priority & total':
            fig.add_trace(go.Scatter(x=waitlist_totalapp['Date'], y=waitlist_totalapp['Value'], mode='lines+markers', name='Total applications', fill='tonexty'))
            fig.add_trace(go.Scatter(x=waitlist_priorityapp['Date'], y=waitlist_priorityapp['Value'], mode='lines+markers', name='Priority applications', line=dict(color='red'), fill='tozeroy', fillcolor='palevioletred'))
            if axis2 == 'Average Number Of Individuals Per Application':
                fig.add_trace(go.Scatter(x=waitlist_averageperapptot['Date'], y=waitlist_averageperapptot['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='Avg persons -total', yaxis='y2'))
            if Show_Rolling:
                fig.add_trace(go.Scatter(x=rolling_avgtotapp['Date'], y=rolling_avgtotapp['Value'], mode='lines', line=dict(color='blue', width=2, dash='dot'), name='12 month rolling average - total'))
        else:
            fig.add_trace(go.Bar(x=waitlist_priorityapp['Date'], y=waitlist_priorityapp['Value'], name='Priority applications', marker_color='red'))
            fig.add_trace(go.Bar(x=waitlist_nonpriorityapp['Date'], y=waitlist_nonpriorityapp['Value'], name='Non-priority applications'))
            fig.add_trace(go.Scatter(x=waitlist_totalapp['Date'], y=waitlist_totalapp['Value'], mode='lines+markers', line=dict(color='black'), name='Total applications'))
            if Show_Rolling:
                fig.add_trace(go.Scatter(x=rolling_avgnonapp['Date'], y=rolling_avgnonapp['Value'], mode='lines', line=dict(color='blue', width=2, dash='dot'), name='12 month rolling average - total'))
            fig.update_layout(barmode='stack')
            if axis2 == 'Average Number Of Individuals Per Application':
                fig.add_trace(go.Scatter(x=waitlist_averageperapptot['Date'], y=waitlist_averageperappnon['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='Avg persons -total', yaxis='y2'))
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgpriapp['Date'], y=rolling_avgpriapp['Value'], mode='lines', line=dict(color='maroon', width=2, dash='dot'), name='12 month rolling average - priority'))
        fig.update_layout(yaxis=dict(title='Applications'))
        if axis2 == 'Proportion of Waitlist that is priority':
            fig.add_trace(go.Scatter(x=waitlist_proportionpriority['Date'], y=waitlist_proportionpriority['Value'], mode='lines',  line=dict(color='maroon', dash='dash', width=2), name='Proportion priority',  yaxis='y2'))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Proportion priority (%)'), showlegend=True, title_text='Waitlist applications and priority percentage')
        elif axis2 == 'Average Number Of Individuals Per Application':
            fig.add_trace(go.Scatter(x=waitlist_averageperapppri['Date'], y=waitlist_averageperapppri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='Avg persons - priority', yaxis='y2'))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Average persons'), showlegend=True, title_text='Waitlist applications and average persons per application')
        else:
            fig.update_layout(showlegend=True, title_text='Waitlist applications')
    else:
        if graph_type == 'Priority & total':
            fig.add_trace(go.Scatter(x=waitlist_totalind['Date'], y=waitlist_totalind['Value'], mode='lines+markers', name='Total individuals', fill='tonexty'))
            fig.add_trace(go.Scatter(x=waitlist_priorityind['Date'], y=waitlist_priorityind['Value'], mode='lines+markers', line=dict(color='red'), name='Priority individuals', fill='tozeroy', fillcolor='palevioletred'))
            fig.update_layout(yaxis=dict(title='Individuals'))
            if Show_Rolling:
                fig.add_trace(go.Scatter(x=rolling_avgtotind['Date'], y=rolling_avgtotind['Value'], mode='lines', line=dict(color='royalblue', width=2, dash='dot'), name='12 month rolling average - total'))
            if axis2 == 'per 10 000':
                fig.add_trace(go.Scatter(x=waitlist_per10000tot['Date'], y=waitlist_per10000tot['Value'], mode='lines', line=dict(color='navy', width=2), name='per 10 000 - total', yaxis='y2'))
            elif axis2 == 'Percentage of population':
                fig.add_trace(go.Scatter(x=waitlist_percentagetot['Date'], y=waitlist_percentagetot['Value'], line=dict(color='navy', width=2), mode='lines+markers', name='% population - total', yaxis='y2'))
        else:
            fig.add_trace(go.Bar(x=waitlist_priorityind['Date'], y=waitlist_priorityind['Value'], name='Priority individuals', marker_color='red'))
            fig.add_trace(go.Bar(x=waitlist_nonpriorityind['Date'], y=waitlist_nonpriorityind['Value'], name='Non-priority individuals'))
            fig.add_trace(go.Scatter(x=waitlist_totalind['Date'], y=waitlist_totalind['Value'], mode='lines+markers', line=dict(color='black'), name='Total individuals'))
            fig.update_layout(barmode='stack')
            if Show_Rolling:
                fig.add_trace(go.Scatter(x=rolling_avgnonind['Date'], y=rolling_avgnonind['Value'], mode='lines', line=dict(color='royalblue', width=2, dash='dot'), name='12 month rolling average - total'))
            if axis2 == 'per 10 000':
                fig.add_trace(go.Scatter(x=waitlist_per10000non['Date'], y=waitlist_per10000non['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='per 10 000 - total', yaxis='y2'))
            elif axis2 == 'Percentage of population':
                fig.add_trace(go.Scatter(x=waitlist_percentagenon['Date'], y=waitlist_percentagenon['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='% population - total', yaxis='y2'))
        fig.update_layout(yaxis=dict(title='Individuals'))
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgpriind['Date'], y=rolling_avgpriind['Value'], mode='lines', line=dict(color='maroon', width=2, dash='dot'), name='12 month rolling average - priority'))
        if axis2 == 'per 10 000':
            fig.add_trace(go.Scatter(x=waitlist_per10000pri['Date'], y=waitlist_per10000pri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='per 10 000 - priority', yaxis='y2'))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='per 10 000 residents'), showlegend=True, title_text='Waitlist individuals and rate per 10 000 residents')
        elif axis2 == 'Percentage of population':
            fig.add_trace(go.Scatter(x=waitlist_percentagepri['Date'], y=waitlist_percentagepri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='% population - priority', yaxis='y2'))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='% population'), showlegend=True, title_text='Waitlist individuals and percentage of population')
        else:
            fig.update_layout(showlegend=True, title_text='Waitlist individuals')

    fig.update_layout(
        xaxis=dict(
            tickformat="%b %y",  # Format for mmm yy
            tick0=waitlist_totalapp['Date'].min(),  # Starting point
            dtick="M3"  # Interval of 3 months
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.1  # Adjust these values to move the legend further away
        ),
    )

    #4 columns
    col1, col2, col3 = st.columns(3)
    with col3:
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)
    return

def waitlist_breakdowns():
    source = pd.read_csv('DATA/SOURCE DATA/Public housing/Waitlist_breakdowns.csv')
    st.markdown(f'Source: <a href="https://www.parliament.wa.gov.au/Parliament/Pquest.nsf/(SearchResultsAllDesc)?SearchView&Query=(Housing%20waitlist)&Start=1&SearchOrder=4&SearchMax=1000">Parliamentary questions</a>', unsafe_allow_html=True)

    data = source.copy()
    #filter data for Item = Dwelling need | New tenancies by region
    data = data[(data['Item'] == 'Dwelling need') | (data['Item'] == 'New tenancies by region') | (data['Item'] == 'Waiting time by region') | (data['Item'] == 'Waiting time by dwelling need')]

    #for columns in DATA, if column name is 'Date', convert to datetime
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

    #create separate dataframe for each Category in column 'Category'

    col1, col2 = st.columns(2)
    with col1:
        view = st.selectbox('Dataset', data['Item'].unique())
    with col2:
        filtered_data = data[data['Item'] == view]
        categories = filtered_data['Category'].unique()     
        categories = ['All'] + list(categories)
        category = st.selectbox('Category', categories)
    with col1:
        if category != 'All':
            filtered_data = filtered_data[filtered_data['Category'] == category]
        subcategories = filtered_data['Subcategory'].unique()
        if len(filtered_data['Subcategory'].unique()) > 1:
            subcategory = st.selectbox('Subcategory', subcategories)
        else:
            subcategory = filtered_data['Subcategory'].unique()[0]
    with col2:
        filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
        if len(filtered_data['Region'].unique()) > 1:
            region = st.selectbox('Region', ['All'] + list(filtered_data['Region'].unique()), index=0)  # Include 'All' option in region selectbox
            if region != 'All':    
                filtered_data = filtered_data[filtered_data['Region'] == region]

    latest_date = filtered_data['Date'].max()
    #convert to dd mmmm yy
    latest_date = latest_date.strftime('%d %B %Y')
    with col2:
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)


    if view == 'Dwelling need':
        datalabels = st.radio('Data labels on bars', ['On', 'Off'], index=1, key='datalabels', horizontal=True)
        if category == 'All':
            dwellingdata = data[data['Item'] == 'Dwelling need']
            categories = dwellingdata['Category'].unique()
            for category in categories:
                st.markdown('**{view} for {category} {subcategory} at {latest_date}**'.format(view=view, category=category, subcategory=subcategory, latest_date=latest_date), unsafe_allow_html=True)
                #filter data to only include latest date
                pie1 = filtered_data[filtered_data['Date'] == latest_date]
                piecat = pie1[pie1['Category'] == category]
                #pie chart of Value by Detail
                fig = px.pie(piecat, values='Value', names='Detail')
                #label Value and %
                if datalabels == 'On':
                    fig.update_traces(texttemplate='%{value:,.0f} (%{percent})', textposition='inside')
                st.plotly_chart(fig)
            for category in categories:
                st.markdown(f'**Dwelling demand by {category} over time**', unsafe_allow_html=True)
                fig2cat = filtered_data[filtered_data['Category'] == category]
                fig2 = go.Figure()
                for Detail in filtered_data['Detail'].unique():
                    fig2filtered_data = fig2cat[fig2cat['Detail'] == Detail]
                    fig2filtered_data['Date'] = fig2filtered_data['Date'].dt.strftime('%d %B %Y')
                    fig2.add_trace(go.Bar(x=fig2filtered_data['Date'], y=fig2filtered_data['Value'], name=Detail))
                if datalabels == 'On':
                    fig2.update_traces(texttemplate='%{y:.0f}', textposition='inside')
                #barmode stack
                fig2.update_layout(barmode='stack', yaxis=dict(title=f'{subcategory}'))
                st.plotly_chart(fig2, use_container_width=True)
            for category in categories:
                st.markdown(f'**Dwelling types needed by {category} - point in time comparison**', unsafe_allow_html=True)
                fig3 = go.Figure()
                cat = filtered_data[filtered_data['Category'] == category]
                dates = cat['Date'].unique()
                for date in dates:
                    fig3filtered_data = cat[cat['Date'] == date]
                    date = date.strftime('%d %B %Y')
                    fig3.add_trace(go.Bar(x=fig3filtered_data['Detail'], y=fig3filtered_data['Value'], name=date))
                if datalabels == 'On':
                    fig3.update_traces(texttemplate='%{y:.0f}', textposition='inside')
                fig3.update_layout(yaxis=dict(title=f'{subcategory}'))
                st.plotly_chart(fig3)
        else:
            st.markdown('**{view} for {category} {subcategory} at {latest_date}**'.format(view=view, category=category, subcategory=subcategory, latest_date=latest_date), unsafe_allow_html=True)
            #filter data to only include latest date
            filtered_filtered_data = filtered_data[filtered_data['Date'] == latest_date]
            #pie chart of Value by Detail
            fig = px.pie(filtered_data, values='Value', names='Detail')
            st.plotly_chart(fig)
            #bar chart of Value by Date, stack by Detail
            fig2 = go.Figure()
            for Detail in filtered_data['Detail'].unique():
                fig2filtered_data = filtered_data[filtered_data['Detail'] == Detail]
                fig2filtered_data['Date'] = fig2filtered_data['Date'].dt.strftime('%d %B %Y')
                fig2.add_trace(go.Bar(x=fig2filtered_data['Date'], y=fig2filtered_data['Value'], name=Detail))
                #label data inside top bar
            if datalabels == 'On':
                fig2.update_traces(texttemplate='%{y:.0f}', textposition='inside')
            #barmode stack
            fig2.update_layout(barmode='stack')

            st.plotly_chart(fig2, use_container_width=True)

            fig3 = go.Figure()
            dates = filtered_data['Date'].unique()
            for date in dates:
                fig3filtered_data = filtered_data[filtered_data['Date'] == date]
                #convert date to string
                date = date.strftime('%d %B %Y')
                fig3.add_trace(go.Bar(x=fig3filtered_data['Detail'], y=fig3filtered_data['Value'], name=date))
            if datalabels == 'On':
                fig3.update_traces(texttemplate='%{y:.0f}', textposition='inside')
            st.plotly_chart(fig3)
        

    elif view == 'New tenancies by region':
        datalabels = st.radio('Data labels on bars', ['On', 'Off'], index=1, key='datalabels', horizontal=True)
        dates = filtered_data['Date'].unique()
        if len(dates) < 2:
            st.markdown('Single data point only')
            #clean = data but drop Subcategory, Detail, Item, Newtenanciestime
            date = filtered_data['Date'].unique()[0]
            clean =data[data['Item'] == view]
            clean = clean.drop(columns=['Subcategory', 'Detail', 'Item', 'Newtenanciestime', 'Date'], axis=1)
            #Date to string
            date = date.strftime('%d %B %Y')
            #if string in Category contains Priority, change to Priority, else Total
            clean['Category'] = clean['Category'].str.contains('Priority')
            clean['Category'] = clean['Category'].replace(True, 'Priority')
            clean['Category'] = clean['Category'].replace(False, 'Total')
            #print clean
            #create Priority and Total columns for each Region
            clean = clean.pivot_table(index='Region', columns='Category', values='Value', aggfunc='sum')
        
            #create WA total row
            clean.loc['WA total'] = clean.sum()    

            clean['Priority %'] = clean['Priority'] / clean['Total'] * 100
            #proportion priority to .1f
            clean['Priority %'] = clean['Priority %'].round(1)
            #get data for item = Region need
            region_need = source[source['Item'] == 'Region need']

            region_dates = region_need['Date'].unique()

            #pick latest date
            latest_date = region_dates.max()
            #filter data to only include latest date
            region_need = region_need[region_need['Date'] == latest_date]

            #if category string contains Priority, change to Priority, else Total
            region_need['Category'] = region_need['Category'].str.contains('Priority')
            region_need['Category'] = region_need['Category'].replace(True, 'Priority')
            region_need['Category'] = region_need['Category'].replace(False, 'Total')
            
            #filter for Subcategory = Applications
            region_need = region_need[region_need['Subcategory'] == 'Applications']
            #drop Subcategory, Detail, Item, Newtenanciestime, Date
            region_need = region_need.drop(columns=['Subcategory', 'Detail', 'Item', 'Newtenanciestime', 'Date'], axis=1)
            #pivot table
            region_need = region_need.pivot_table(index='Region', columns='Category', values='Value', aggfunc='sum')
            #create WA total row
            region_need.loc['WA total'] = region_need.sum()
            region_need['Priority %'] = region_need['Priority'] / region_need['Total'] * 100
            #proportion priority to .1f
            region_need['Priority %'] = region_need['Priority %'].round(1)
            #merge clean and region_need
            clean = pd.merge(clean, region_need, on='Region', suffixes=('', ' waitlist'))
            clean[f'% housed - Priority'] = clean['Priority'] / clean['Priority waitlist'] * 100
            clean[f'% housed - Priority'] = clean[f'% housed - Priority'].round(1)

            clean[f'% housed - Total'] = clean['Total'] / clean['Total waitlist'] * 100
            clean[f'% housed - Total'] = clean[f'% housed - Total'].round(1)
            # regionfigdata = clean but region as column not index
            regionfigdata = clean.reset_index()
            regionfig = go.Figure()
            regionfig.add_trace(go.Bar(x=regionfigdata['Region'], y=regionfigdata[f'% housed - Priority'], name=f'% housed - Priority'))
            regionfig.add_trace(go.Bar(x=regionfigdata['Region'], y=regionfigdata[f'% housed - Total'], name=f'% housed - Total'))
            regionfig.update_layout(barmode='group', yaxis=dict(title='%'), title_text = f'Percentage of waitlist at {latest_date} housed in 12months to to {date} - group by region')
            #data labels inside top bar
            if datalabels == 'On':
                regionfig.update_traces(texttemplate='%{y:.1f}', textposition='inside')
            st.plotly_chart(regionfig)
            regionlist = list(regionfigdata['Region'].unique())
            # plot a version with region as traces and % housed categories as y groups
            housed = regionfigdata[['Region', '% housed - Priority', '% housed - Total']]
            #transpose housed
            housed = housed.T
            #reset index
            housed = housed.reset_index()
            #row 0 as column names
            housed.columns = housed.iloc[0]
            #drop row 0
            housed = housed.drop(0)
            #rename Region to Category
            housed = housed.rename(columns={'Region': 'Category'})

            regionfig2 = go.Figure()
            for region in regionlist:
                regionfig2.add_trace(go.Bar(x=housed['Category'], y=housed[region], name=region))
            regionfig2.update_layout(barmode='group', yaxis=dict(title='%'), title_text = f'Percentage of waitlist at {latest_date} housed in 12 months to {date} - group by applicant type')
            if datalabels == 'On':
                regionfig2.update_traces(texttemplate='%{y:.1f}', textposition='inside')
            st.plotly_chart(regionfig2)



            st.write(housed)

            st.write(clean)
        else:
            for region in filtered_data['Region'].unique():
                st.markdown(f'**New tenancies in {region}**', unsafe_allow_html=True)
                regionchart = go.Figure()
                region_filtered_data = filtered_data[filtered_data['Region'] == region]
                region_filtered_data['Date'] = region_filtered_data['Date'].dt.strftime('%d %B %Y')
                regionchart.add_trace(go.Bar(x=region_filtered_data['Date'], y=region_filtered_data['Value'], name=region))
                regionchart.update_layout(yaxis=dict(title='New tenancies'))
                st.plotly_chart(regionchart, use_container_width=True)

    elif view == 'Waiting time by dwelling need':
        #if Category contains Priority, change to Priority, else Total
        filtered_data['Category'] = filtered_data['Category'].str.contains('Priority')
        filtered_data['Category'] = filtered_data['Category'].replace(True, 'Priority Waitlist')
        filtered_data['Category'] = filtered_data['Category'].replace(False, 'Total Waitlist')
        #if len Subcategory >1 selectbox
        if len(filtered_data['Subcategory'].unique()) > 1:
            #selectbox Subcategory
            subcategory = st.selectbox('Metric', filtered_data['Subcategory'].unique())
            #filter data to only include selected Subcategory
            filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
            #drop Subcategory
            filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
        else:
            #drop Subcategory
            filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
        #drop Item, Newtenanciestime, Region
        filtered_data = filtered_data.drop(columns=['Item', 'Newtenanciestime', 'Region'], axis=1)
        #pivot table
        #round value to .0f
        filtered_data['Value'] = filtered_data['Value'].round(0)
        #date as string
        filtered_data['Date'] = filtered_data['Date'].dt.strftime('%d %B %Y')
        dwellingwait = go.Figure()
        if len(filtered_data['Date'].unique()) ==1:
            date = filtered_data['Date'].unique()[0]
            for category in filtered_data['Category'].unique():
                categorydata = filtered_data[filtered_data['Category'] == category]
                dwellingwait.add_trace(go.Bar(x=categorydata['Detail'], y=categorydata['Value'], name=category))
            dwellingwait.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {date}')
            st.plotly_chart(dwellingwait, use_container_width=True)
        else:
            if category != 'All':
                for date in filtered_data['Date'].unique():
                    datefiltered_data = filtered_data[filtered_data['Date'] == date]
                    dwellingwait.add_trace(go.Bar(x=datefiltered_data['Detail'], y=datefiltered_data['Value'], name=date))
                dwellingwait.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {category}', showlegend=True)
            else:
                for cat in filtered_data['Category'].unique():
                    catwaitdwellfig = go.Figure()
                    catfiltered_data = filtered_data[filtered_data['Category'] == cat]
                    for date in catfiltered_data['Date'].unique():
                        datefiltered_data = catfiltered_data[catfiltered_data['Date'] == date]
                        catwaitdwellfig.add_trace(go.Bar(x=datefiltered_data['Detail'], y=datefiltered_data['Value'], name=date))
                    catwaitdwellfig.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {cat}', showlegend=True)
                    st.plotly_chart(catwaitdwellfig, use_container_width=True)
        
        
        whenjoinorhouse = filtered_data.copy()
        #add column Forecast house date = today + weeks(Value)
        whenjoinorhouse['Forecast house date'] = pd.to_datetime(whenjoinorhouse['Date']) + pd.to_timedelta(whenjoinorhouse['Value'], unit='w')
        #add column Backcast apply date = today - weeks(Value)
        whenjoinorhouse['Backcast apply date'] = pd.to_datetime(whenjoinorhouse['Date']) - pd.to_timedelta(whenjoinorhouse['Value'], unit='w')
        #set columns to string 
        whenjoinorhouse['Forecast house date'] = whenjoinorhouse['Forecast house date'].dt.strftime('%d %B %Y')
        whenjoinorhouse['Backcast apply date'] = whenjoinorhouse['Backcast apply date'].dt.strftime('%d %B %Y')
        st.write(whenjoinorhouse)

    elif view == 'Waiting time by region':
        #repeat similar to above
        #if Category contains Priority, change to Priority, else Total
        filtered_data['Category'] = filtered_data['Category'].str.contains('Priority')
        filtered_data['Category'] = filtered_data['Category'].replace(True, 'Priority Waitlist')
        filtered_data['Category'] = filtered_data['Category'].replace(False, 'Total Waitlist')
        #if len Subcategory >1 selectbox
        if len(filtered_data['Subcategory'].unique()) > 1:
            #selectbox Subcategory
            subcategory = st.selectbox('Metric', filtered_data['Subcategory'].unique())
            #filter data to only include selected Subcategory
            filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
            #drop Subcategory
            filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
        else:
            #drop Subcategory
            filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)

        #drop Item, Newtenanciestime, Detail
        filtered_data = filtered_data.drop(columns=['Item', 'Newtenanciestime', 'Detail'], axis=1)
        #pivot table
        #round value to .0f
        filtered_data['Value'] = filtered_data['Value'].round(0)
        #forecast house date = today + weeks(Value)
        filtered_data['Forecast house date'] = pd.to_datetime(filtered_data['Date']) + pd.to_timedelta(filtered_data['Value'], unit='w')
        #backcast apply date = today - weeks(Value)
        filtered_data['Backcast apply date'] = pd.to_datetime(filtered_data['Date']) - pd.to_timedelta(filtered_data['Value'], unit='w')
        #set columns to string
        filtered_data['Date'] = filtered_data['Date'].dt.strftime('%d %B %Y')
        filtered_data['Forecast house date'] = filtered_data['Forecast house date'].dt.strftime('%d %B %Y')
        filtered_data['Backcast apply date'] = filtered_data['Backcast apply date'].dt.strftime('%d %B %Y')
        st.write(filtered_data)
        return
    
def show_update_log():
    update_log = pd.read_excel('DATA/SOURCE DATA/update_log.xlsx')

    st.write('Update Log')
    st.table(update_log)
    return

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

def ROGS_sector():
    df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G.csv', encoding='latin-1')
    #sort year ascending
    df = df.sort_values(by='Year', ascending=True)
    df['Year'] = df['Year'].astype(str)

    st.markdown(f'Source: <a href="https://www.pc.gov.au/research/ongoing/report-on-government-services/2022/housing-and-homelessness">Report on Government Services 2023, Part G, Sector Overview</a>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
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
        datalabels = st.radio('Data labels', ['On', 'Off'], index=0, horizontal=True)
    with col3:
        st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

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
        st.plotly_chart(fig)

        fig2 = go.Figure()
        for region in regions_sector:
            fig2.add_trace(go.Bar(x=CRA['Year'], y=CRA[region], name=region))
        fig2.update_layout(barmode='group', title='CRA funding', yaxis_title=ytitle)
        #legend below chart
        fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=1))
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
        with col2:
            select_view = st.selectbox('Select view', ['Demographics', 'Housing affordability'])
        if select_view == 'Demographics':
            #in Description2, replace "Income unit" with "family type"
            df['Description2'] = df['Description2'].str.replace('Income unit', 'Family type')
            #replace All with Support payment type
            df['Description2'] = df['Description2'].str.replace('All', 'Support payment type')
            df['Description2'] = df['Description2'].str.replace('Aged under 25 years', 'Aged under 25 / aged over 75')
            df['Description2'] = df['Description2'].str.replace('Aged 75 years or over', 'Aged under 25 / aged over 75')
            #remove from Description2: Major cities Inner regional Outer regional Remote Very remote, Disability Support Pension recipient, Non-Indigenous, Dependent children in income units
            df= df[df['Description2'] != 'Major cities']
            df= df[df['Description2'] != 'Inner regional']
            df= df[df['Description2'] != 'Outer regional']
            df= df[df['Description2'] != 'Remote']
            df= df[df['Description2'] != 'Very remote']
            df= df[df['Description2'] != 'Disability Support Pension recipient']
            df= df[df['Description2'] != 'Non-Indigenous']
            df= df[df['Description2'] != 'Dependent children in income units']
            
            


            col1, col2 = st.columns(2)
            df = df[df['Description1'] == 'Income units receiving CRA']
            with col1:
                select_sector = st.selectbox('Detail', df['Description2'].unique())
                df = df[df['Description2'] == select_sector]
                if select_sector == 'Paying enough rent to be eligible for maximum assistance':
                    df = df[df['Description2'] == select_sector]
                    #allow select region, select year
                    with col1:
                        select_years_sector = st.multiselect('Select year', df['Year'].unique(), default=df['Year'].unique())
                    df = df[df['Year'].isin(select_years_sector)]
                    fig = go.Figure()
                    #for region in regions, add trace to fig
                    for region in regions:
                        fig.add_trace(go.Bar(x=df['Year'], y=df[region], name=region))
                    fig.update_layout(barmode='group', title='Paying enough rent to be eligible for maximum assistance', xaxis_title="Year", yaxis_title="%")
                    #add data labels inside bars
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                if select_sector == 'Geographic location':
                    
                    #select year
                    with col1:
                        select_years_geo = st.multiselect('Select year', df['Year'].unique(), default=df['Year'].unique())
                    with col2:
                        select_unit = st.selectbox('Select unit', df['Unit'].unique())
                    df = df[df['Year'].isin(select_years_geo)]
                    df = df[df['Unit'] == select_unit]
                    fig = go.Figure()
                    for region in regions:
                        fig.add_trace(go.Bar(x=[df['Description3'],df['Year']], y=df[region], name=region))
                    #add figure inside bar
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    fig.update_layout(barmode='group', title='By geographic location', xaxis_title="Year", yaxis_title=select_unit)
                    st.plotly_chart(fig)
                if select_sector == 'Total':
                    df = df[df['Description2'] == select_sector]
                    fig = go.Figure()
                    for region in regions:
                        fig.add_trace(go.Bar(x=df['Year'], y=df[region], name=region))
                    fig.update_layout(barmode='group', title='Total receiving CRA', xaxis_title="Year", yaxis_title=df['Unit'].unique()[0])
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                if select_sector == "Aboriginal and Torres Strait Islander":
                    df = df[df['Description2'] == select_sector]
                    df1 = df[df['Table_Number'] == 'GA.8']
                    df2 = df[df['Table_Number'] == 'GA.9']
                    a8list = df1['Description3'].unique().tolist()
                    #remove total
                    a8list.remove('Total')
                    fig = go.Figure()
                    df1pc = df1[df1['Unit'] == '%']
                    df1no = df1[df1['Unit'] == 'no.']
                    for region in regions:
                        fig.add_trace(go.Bar(x=df1pc['Description3'], y=df1pc[region], name=region))
                    fig.update_layout(barmode='stack', title='Aboriginal and Torres Strait Islander recipient family types - %', xaxis_title="Family type", yaxis_title='%')
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                    fig2 = go.Figure()
                    for region in regions:
                        fig2.add_trace(go.Bar(x=df1no['Description3'], y=df1no[region], name=region))
                    fig2.update_layout(barmode='stack', title='Aboriginal and Torres Strait Islander recipient family types - no.', xaxis_title="Family type", yaxis_title='no.')
                    if datalabels == 'On':
                        fig2.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig2)
                    fig3 = go.Figure()
                    for region in regions:
                        fig3.add_trace(go.Bar(x=df2['Description3'], y=df2[region], name=region))
                    fig3.update_layout(barmode='stack', title='Aboriginal and Torres Strait Islander recipient payment types - %', xaxis_title="Payment type", yaxis_title='%')
                    if datalabels == 'On':
                        fig3.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig3)
                if select_sector == "Support payment type":
                    df = df[df['Description2'] == select_sector]
                    fig = go.Figure()
                    for region in regions:
                        fig.add_trace(go.Bar(x=df['Description3'], y=df[region], name=region))
                    fig.update_layout(barmode='group', title='Support payment type', xaxis_title="Payment type", yaxis_title='%')
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                if select_sector == "Aged under 25 / aged over 75":
                    df = df[df['Description2'] == select_sector]
                    dfpc = df[df['Unit'] == '%']
                    dfno = df[df['Unit'] == 'no.']
                    fig = go.Figure()
                    for region in regions:
                        fig.add_trace(go.Bar(x=dfpc['Description2'], y=dfpc[region], name=region))
                    fig.update_layout(barmode='group', title='Aged under 25 and aged over 75', xaxis_title="Age group", yaxis_title='%')
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                    fig2 = go.Figure()
                    for region in regions:
                        fig2.add_trace(go.Bar(x=dfno['Description2'], y=dfno[region], name=region))
                    fig2.update_layout(barmode='group', title='Aged under 25 and aged over 75', xaxis_title="Age group", yaxis_title='no.')
                    if datalabels == 'On':
                        fig2.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig2)
                if select_sector == "Family type":
                    df = df[df['Description2'] == select_sector]
                    dfpc = df[df['Unit'] == '%']
                    dfno = df[df['Unit'] == 'no.']
                    fig = go.Figure()
                    for region in regions:
                        fig.add_trace(go.Bar(x=dfpc['Description3'], y=dfpc[region], name=region))
                    fig.update_layout(barmode='group', title='Family type', xaxis_title="Family type", yaxis_title='%')
                    if datalabels == 'On':
                        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig)
                    fig2 = go.Figure()
                    for region in regions:
                        fig2.add_trace(go.Bar(x=dfno['Description3'], y=dfno[region], name=region))
                    fig2.update_layout(barmode='group', title='Family type', xaxis_title="Family type", yaxis_title='no.')
                    if datalabels == 'On':
                        fig2.update_traces(texttemplate='%{y:.2s}', textposition='inside')
                    st.plotly_chart(fig2)
        elif select_view == 'Housing affordability':
        #Description1 = Income units receiving CRA at 30 June
            df= df[df['Description1'] == 'Income units receiving CRA at 30 June']
            #sort year ascending
            df = df.sort_values(by=['Year'], ascending=True)
            #if Equity_Group null copy from Remoteness
            df['Equity_Group'] = df['Equity_Group'].fillna(df['Remoteness'])
            with col2:
                ha_filter = st.selectbox('Select group', df['Equity_Group'].unique(), index=4)
            df = df[df['Equity_Group'] == ha_filter]
            df1 = df[df['Description2'] == 'Paying more than 30% of income on rent']
            df2 = df[df['Description2'] == 'Paying more than 50% of income on rent']
            fig = go.Figure()
            for region in regions:
                fig.add_trace(go.Bar(x=[df1['Description4'], df['Year']], y=df1[region], name=region))
            fig.update_layout(barmode='group', title='Proportion recipients paying more than 30% of income on rent', yaxis_title='%')
            if datalabels == 'On':
                fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
            st.plotly_chart(fig)
            fig2 = go.Figure()
            for region in regions:
                fig2.add_trace(go.Bar(x=[df2['Description4'], df['Year']], y=df2[region], name=region))
            fig2.update_layout(barmode='group', title='Proportion recipients paying more than 50% of income on rent', yaxis_title='%')
            if datalabels == 'On':
                fig2.update_traces(texttemplate='%{y:.2s}', textposition='inside')
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

    #sort Year ascending
    rogshousing = rogshousing.sort_values(by='Year', ascending=True)

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
    #sort year ascending
    df = df.sort_values(by='Year', ascending=True)
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

    if select_measure == "Homelessness; by homelessness operational group":
        #fill Description2 null with persons
        df['Description2'] = df['Description2'].fillna('Persons')
        col1, col2, col3 = st.columns(3)
        with col1:
            Desc2 = st.selectbox('Select Description2 filter', df['Description2'].unique(), index=0)
            df = df[df['Description2'] == Desc2]
        with col2:
            if len(df['Description3'].unique()) > 1:
                Desc3 = st.selectbox('Select Description3 filter', df['Description3'].unique(), index=0)
                df = df[df['Description3'] == Desc3]
        with col3:
            if len(df['Description4'].unique()) > 1:
                Desc4 = st.selectbox('Select Description4 filter', df['Description4'].unique(), index=0)
                df = df[df['Description4'] == Desc4]

        #sort Year ascending
        df = df.sort_values(by=['Year'], ascending=True)
        #for region in regions, filter df for region, plotly bar, x=Year, y=Value, color=Region, group
        fig = go.Figure()
        yunits = df['Unit'].unique()[0]
        for region in regions:
            fig.add_trace(go.Bar(x=df['Year'], y=df[region], name=region))
        fig.update_layout(barmode='group', title='Homelessness; by homelessness operational group', xaxis_title="Year", yaxis_title=yunits)
        

        st.plotly_chart(fig)

    return

def external_resources():
    external = pd.read_excel('assets/External.xlsx', sheet_name='Sheet1')

    #button that points to , text = By-name list
    st.markdown(f'<h3><a href ="https://www.endhomelessnesswa.com/bynamelist-datapage">Visit by-name list site </a></h3>', unsafe_allow_html=True)

    for i in external.index:
        file = 'assets/' + external['File'][i]
        #display file - png 
        st.markdown(f'<h3>2023 housing affordability charts from Anglicare WA</h3>', unsafe_allow_html=True)
        st.markdown(f'<h5>{external["caption"][i]}</h5>', unsafe_allow_html=True)
        st.image(file, use_column_width=True)
        st.markdown(f'<a href="{external["Reference link"][i]}">Source: {external["Reference text"][i]}</a>', unsafe_allow_html=True)
    return

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

if __name__ == "__main__":
    home()

