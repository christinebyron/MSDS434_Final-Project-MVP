# -*- coding: utf-8 -*-
"""Byron, Christine_MSDS 434_NY Citi Bike_Logistic Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XXHcZLioT6l4SromXtmMVRuk4s4jdVBf

#Final Assignment - NYC Citi Bike Trips

**Overview**


After having analyzed our Citi Bike Usres, it was evident that there were some wins that could be delivered to those that purchase daily or three-day passes. Our goal was to futher analyze this data so that we could attempt to build an application that better supported them making the best decision for there specific use case.

###Notebook Setup
"""

from google.colab import auth
auth.authenticate_user()
print('Authenticated')

#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import *
import seaborn as sns
from matplotlib import rcParams
import datetime as dt
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import vincenty
from geopy import distance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler



"""###Analyze Citi Bike - Customer Data

After having cleaned an analyzed the larger Citi Bike dataset, a subset of 32,800 Customer records was generated for further exploratory research. The details below show the how this sample count was created.
"""

project_id = 'msds434-cohort-analysis-mvp'

from google.cloud import bigquery

client = bigquery.Client(project='msds434-cohort-analysis-mvp')

sample_count = 32800
row_count = client.query('''
  SELECT 
    COUNT(*) as total
  FROM `msds434-cohort-analysis-mvp.citibikenyc_analysis.citibikenyc_customer`''').to_dataframe().total[0]

df = client.query('''
  SELECT
    *
  FROM
    `msds434-cohort-analysis-mvp.citibikenyc_analysis.citibikenyc_customer`
  WHERE RAND() < %d/%d
''' % (sample_count, row_count)).to_dataframe()

print('Full dataset has %d rows' % row_count)

df.describe()

"""####Data Clean Up

**Missing Data**: Confirm all missing data is removed from the dataset.
"""

sample_df = df
#Percentage of missing data.
def missing_data(sample_df):
    total = sample_df.isnull().sum().sort_values(ascending=False)
    percent = (sample_df.isnull().sum()/sample_df.isnull().count()*100).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data
missing_data(sample_df)

"""**Data Formatting:** In continuing to prep our Citi Bike data, establish formats will especially help will visualizaton needs."""

#Ensure data is formatted correctly to avoid errors in the visuals
sample_df['starttime'] = to_datetime(sample_df['starttime'])
sample_df['stoptime'] = to_datetime(sample_df['stoptime'])
sample_df['start_station_name'] = sample_df['start_station_name'].astype('category')
sample_df['end_station_name'] = sample_df['end_station_name'].astype('category')
sample_df['usertype'] = sample_df['usertype'].astype('category')
sample_df['gender'] = sample_df['gender'].astype('category')
round(sample_df.describe(),2)

"""###Explore Key Variables

####Top 5 Citi Bike Stations

Let's review the top 5 stations for our Customer user types.
"""

#Data for Top 5 Stations visual
top5 = pd.DataFrame() 
top5['station']=sample_df['start_station_name'].value_counts().head().index
top5['number_of_starts']=sample_df['start_station_name'].value_counts().head().values
top5['station'] = top5['station'].cat.remove_unused_categories()
top5['station'] = top5['station'].astype('object')
#top5.sort_values(by = 'number_of_starts', ascending = False)

#Plot for Part 1: Top 5 Stations
ax = sns.barplot('station', 'number_of_starts', data = top5, palette="GnBu_d")
ax.set_title('Top 5 Citi Bike Stations for Customers', fontsize = 12)
rcParams['figure.figsize'] = 12,7
ax.set_xticklabels(ax.get_xticklabels(),rotation=40, ha = 'right')
for index, row in top5.iterrows():
    ax.text(index,row['number_of_starts']-4000,row['number_of_starts'], 
            color='white', ha="center", fontsize = 10)
plt.show()

"""###Trip Duration by User Type

Other information that could be important for our prediction model will be the how each user type interacts with Citi bike.
"""

#Calculate trip duration
TD_user = pd.DataFrame()
TD_user['averagminutes'] = round(sample_df.groupby('usertype')['minutes'].mean(),2)
TD_user = TD_user.reset_index()
TD_user['usertype'] = TD_user['usertype'].astype('object')

#Average trip Duration per User Type
ax2 = sns.barplot('usertype', 'averagminutes', data = TD_user,palette="GnBu_d")
ax2.set_title('Average Trip Duration for Customers')
#rcParams['figure.figsize'] = 12,7
ax2.set_xticklabels(ax2.get_xticklabels(),rotation=40, ha = 'right')
ax2.set_ylabel('averagminutes (Minutes)')
for index, row in TD_user.iterrows():
    ax2.text(index,row['averagminutes']-70,(str(row['averagminutes'])), 
             color='white', ha="center", fontsize = 10)
plt.show()

#Boxplots are more informative to visualize breakdown of data
df.boxplot('minutes', by = 'usertype')
plt.show()

"""Research suggest that our customers average at the 30 minute mark. This is important to note given that 30 minutes is the when different pricing models take affect.

####Most Popular Trips

Research also indicates that it could be wise to assess the most poopular trips for our dataset, so we can assess which start and end location might require a 3-day pass to avoid charges over 30-minutes.
"""

#Identify the 10 most popular trips
trips_df = pd.DataFrame()
trips_df = sample_df.groupby(['start_station_name','end_station_name']).size().reset_index(name = 'numberoftrips')
trips_df = trips_df.sort_values('numberoftrips', ascending = False)
trips_df["start_station_name"] = trips_df["start_station_name"].astype(str)
trips_df["end_station_name"] = trips_df["end_station_name"].astype(str)
trips_df["trip"] = trips_df["start_station_name"] + " to " + trips_df["end_station_name"]
trips_df = trips_df[:10]
trips_df = trips_df.drop(['start_station_name', "end_station_name"], axis = 1)
trips_df = trips_df.reset_index()
#trips_df.head()

ax3 = sns.barplot('numberoftrips','trip', data = trips_df,palette="GnBu_d")
ax3.set_title('Most Popular Trips', fontsize = 20)
ax3.set_ylabel("trip",fontsize=16)
ax3.set_xlabel("numberoftrips",fontsize=16)
for index, row in trips_df.iterrows():
    ax3.text(row['numberoftrips']-220,index,row['numberoftrips'], 
             color='white', ha="center",fontsize = 10)
plt.show()

"""####Rider Performance by Age and Gender

Knowing how age and gender coorelates to performance will also be helpful for future modeling efforts
"""

#Combine coordinates to calculate distance 
sample_df['start_coordinates'] = list(zip(sample_df['start_station_latitude'], sample_df['start_station_longitude']))
sample_df['end_coordinates'] = list(zip(sample_df['end_station_latitude'], sample_df['end_station_longitude']))

#Replace missing birth year by median based on speed and gender
sample_df['birth_year'] = sample_df.groupby(['gender','start_station_id'])['birth_year'].transform(lambda x: x.fillna(x.median()))

#if there are still a few nulls, drop these
sample_df = sample_df.dropna(subset=['birth_year'])

#Calculate age and drop circular/roundtrips
sample_df['age'] = 2020 - sample_df['birth_year']
sample_df['age'] = sample_df['age'].astype(int)

dist = [] 
 for i in range(len(sample_df)): 
   dist.append(geopy.distance.vincenty(sample_df.iloc[i]['start_coordinates'],sample_df.iloc[i]['end_coordinates']).miles)
if (i%1000000==0): 
  print(i)

sample_df['distance'] = dist

sample_df = sample_df.drop(sample_df.index[(sample_df['distance'] == 0)])

#df[df['Trip Duration']<90]
#2. Followed the same reasoning as behind Birth Year. People in similar locations tend to also work in a similar industry or location
sample_df['distance'] = sample_df.groupby(['gender','start_station_id'])['distance'].transform(lambda x: x.fillna(x.median()))

sample_df['min_mile'] = round(sample_df['minutes']/sample_df['distance'], 2)
sample_df['mile_hour'] = round(sample_df['distance']/(sample_df['minutes']/60),2)

#Check for Data Integrity
round(sample_df.describe(),2)

#Rider performance by age and Gender in Min/Mile 
fig, ax4 = plt.subplots(figsize=(11,5))
sample_df.groupby(['age','gender']).median()['min_mile'].unstack().plot(ax=ax4, color ="bg")
ax4.legend(['Female','Male'])
plt.ylabel('Median Speed (min/mile)')
plt.title('Rider Performance Based on Gender and Age (Median Speed in min/mile)')
plt.show()

"""##Predictive Modeling

Now that the data is cleaned an dunderstood, we can begin to build a model that predicts how long a trip will take given a starting point and destination.
"""

model_1_df = sample_df

#create a random sample 
model_1_df = model_df.sample(frac = 0.1, random_state = 0)

model_1_df.columns.values

def drop_data(model_1_df):
    model_1_df = model_1_df.drop(['tripduration','stoptime','start_station_id','start_station_latitude','start_station_longitude',
                  'start_coordinates','end_station_id', 'end_station_latitude', 'end_station_longitude', 
                  'end_coordinates','bikeid', 'start_station_name','birth_year','end_station_name','min_mile',
                  'mile_hour','season', 'dayofweek', 'age', 'hour'], axis = 1)
    return model_1_df

df_basemodel = drop_data(model_1_df)

df_basemodel = df_basemodel.drop('starttime', axis =1)

#Dummify categorical data and avoid dummy variable trap
df_basemodel = pd.get_dummies(df_basemodel, drop_first = True)

#review correlation
df_basemodel.corr().loc[:,'minutes']

#Train Test Split
#Predictor variable
X = df_basemodel.iloc[:,1:]
#Target variable
y = df_basemodel.iloc[:,0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

regressor = LinearRegression()
regressor.fit(X_train, y_train)
regressor.score(X_test,y_test)

X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)
regressor_OLS = sm.OLS(y_train, X_train).fit()
regressor_OLS.summary()

"""Continue to refine this model by reviewing date. 
*   December - Feb. = Winter
*   March - May = Spring
*   June - Aug. = Summer
*   Sept. - Nov. = Fall
"""

model_2_df = sample_df

def get_date_info(model_2_df):
    model_2_df['d_week'] = model_2_df['starttime'].dt.dayofweek
    model_2_df['m_yr'] = model_2_df['starttime'].dt.month
    model_2_df['ToD'] = model_2_df['starttime'].dt.hour

    model_2_df['d_week'] = (model_2_df['d_week']<5).astype(int)

    model_2_df['m_yr'] = model_2_df['m_yr'].replace(to_replace=[12,1,2], value = 0)
    model_2_df['m_yr'] = model_2_df['m_yr'].replace(to_replace=[3,4,5], value = 1)
    model_2_df['m_yr'] = model_2_df['m_yr'].replace(to_replace=[6,7,8], value = 2)
    model_2_df['m_yr'] = model_2_df['m_yr'].replace(to_replace=[9,10,11], value = 3)
    
    model_2_df['ToD'] = pd.cut(model_2_df['ToD'], bins=[-1, 5, 9, 14, 20, 25], labels=['Night','Morning','Afternoon','Evening','Night1'])
    model_2_df['ToD'] = model_2_df['ToD'].replace(to_replace='Night1', value = 'Night')
    model_2_df['ToD'] = model_2_df['ToD'].cat.remove_unused_categories()
    
    model_2_df['m_yr'] = model_2_df['m_yr'].astype('category')
    model_2_df['d_week'] = model_2_df['d_week'].astype('category')

    return(model_2_df)

#Dataset for the second model
df_model2 = drop_data(model_2_df)
df_model2 = get_date_info(df_model2)
df_model2 = df_model2.drop('starttime', axis =1)

#Dummify categorical data and avoid dummy variable trap
df_model2 = pd.get_dummies(df_model2, drop_first = True)

#review correlation
df_model2.corr().loc[:,'minutes']

#Predictor variable
X = df_model2.iloc[:,1:]
#Target variable
y = df_model2.iloc[:,0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#Fit Linear Regression and check accuracy using sklearn
regressor = LinearRegression()
regressor.fit(X_train, y_train)
regressor.score(X_test,y_test)

X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)
regressor_OLS = sm.OLS(y_train, X_train).fit()
regressor_OLS.summary()

"""Let's start to look at Start and End Locations"""

model_3_df = sample_df

def drop_data(model_1_df):
    model_1_df = model_1_df.drop(['tripduration','stoptime','distance','start_station_latitude','start_station_longitude',
                  'start_coordinates','end_station_latitude', 'end_station_longitude', 
                  'end_coordinates','bikeid', 'start_station_name','birth_year','end_station_name','min_mile',
                  'mile_hour','season', 'dayofweek', 'age', 'hour'], axis = 1)
    return model_1_df

df_basemodel = drop_data(model_3_df)

def get_date_info(model_3_df):
    model_3_df['d_week'] = model_3_df['starttime'].dt.dayofweek

    model_3_df['d_week'] = (model_3_df['d_week']<5).astype(int)

    return(model_3_df)

#Dataset for the second model
df_model3 = drop_data(model_3_df)
df_model3 = get_date_info(df_model3)
df_model3 = df_model3.drop('starttime', axis =1)

#Dummify categorical data and avoid dummy variable trap
df_model3 = pd.get_dummies(df_model3, drop_first = True)

#review correlation
df_model3.corr().loc[:,'minutes']

#Predictor variable
X = df_model3.iloc[:,1:]
#Target variable
y = df_model3.iloc[:,0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#Fit Linear Regression and check accuracy using sklearn
regressor = LinearRegression()
regressor.fit(X_train, y_train)
regressor.score(X_test,y_test)

X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)
regressor_OLS = sm.OLS(y_train, X_train).fit()
regressor_OLS.summary()

"""Let's continue to explore this logistic regression using AutoML Tables"""