#!/usr/bin/env python

"""
Commandline tool for interacting with library
"""

import pickle 
from google.cloud import storage 
import pandas as pd
from flask import Flask, jsonify, request
import sklearn

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = request.get_json(force=True)

    # convert data into dataframe
    data.update((x, [y]) for x, y in data.items())
    data_df = pd.DataFrame.from_dict(data)
    
    # set up access to the GCS bucket
    bucket_name = "citibikenyc_app"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    # download and load the model
    blob = bucket.blob("sMSDS434_Final-Project-MVP")
    blob.download_to_filename("/tmp/lmodel.pkl")
    model = pk.load(open("/tmp/model.pkl", 'rb'))

    # predictions
    result = model.predict(data_df)

    # send back to browser
    output = {'results': int(result[0])}
     
    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
