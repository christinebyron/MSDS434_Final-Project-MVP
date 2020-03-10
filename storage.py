#!/usr/bin/env python

"""
Commandline tool for interacting with library
"""

from google.cloud import storage

bucket_name = "citibikenyc_app"
storage_client = storage.Client()
storage_client.create_bucket(bucket_name)
for bucket in storage_client.list_buckets():
    print(bucket.name)
