# -*- coding: utf-8 -*-
"""tests.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AQel8p7LR5VTbcDIni2CDE6ndEaeq14m

#Test Flask in Production
"""

import requests
import json

# local url
url = 'http://127.0.0.1:5000/'

# test data
data = {  'start_station_id': 250
             , 'end_station_id': 110
             , 'gender': 1
             , 'dayofweek': 5}

data = json.dumps(data)
data

r_survey = requests.post(url, data)
print(r_survey)

send_request = requests.post(url, data)
print(send_request)

print(send_request.json())

"""#Test App in Heroku"""

# heroku url
heroku_url = 'https://msds434-citibikenyc.herokuapp.com/' 

# test data
data = {'start_station_id': 250
      , 'end_station_id': 110
      , 'gender': 1
      , 'dayofweek': 5}

data = json.dumps(data)
data

# check response code
r_survey = requests.post(heroku_url, data)
print(r_survey)

# get prediction
print(send_request.json())