#!/usr/bin/env python

"""
Commandline tool for interacting with library
"""

import pandas as pd
from flask import Flask, jsonify, request
import pickle

# load model
with open('MSDS434_Final-Project-MVP/model.pkl', 'rb') as file:
    model = pickle.load(file)

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

    # predictions
    result = model.predict(data_df)

    # send back to browser
    output = {'results': int(result[0])}

    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
