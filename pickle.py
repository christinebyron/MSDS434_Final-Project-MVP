#!/usr/bin/env python

"""
Commandline tool for interacting with library
"""

import pickle 
from google.cloud import storage

bucket_name = "citibikenyc_app"
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob("MSDS434_Final-Project-MVP")
blob.download_to_filename("model.pkl")
model = pickle.load(open("model.pkl", 'rb'))
