import pandas as pd
import streamlit as st

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