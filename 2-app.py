import os
import time
import torch
from transformers import pipeline
import streamlit as st
import boto3

s3 = boto3.client('s3')

bucket_name = "tinybertaws"

local_path = 'DEPLOY_MODEL_STREAMLIT/downloads/tinybert-sentiment-analysis'
s3_pefix = 'mlmodel-aws/tinybert-sentiment-analysis/'

def download_folder(local_path, s3_prefix, bucket_name):
    os.makedirs(local_path, exist_ok=True)

    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
        if 'Contents' in result:
            for Key in result['Contents']:
                s3_key = Key['Key']

                local_file = os.path.join(local_path, os.path.relpath(s3_key, s3_prefix))
                os.makedirs(os.path.dirname(local_file), exist_ok=True)

                s3.download_file(bucket_name, s3_key, local_file)

st.title("Machine Learning Model Deployment At The Server !!!")
button = st.button("Download Model")

if button:
    with st.spinner("Downloading........... Please Wait"):
        download_folder(local_path, s3_pefix, bucket_name)
        st.text("Model Downloading finished 😊😊😊")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
classifier = pipeline('text-classification', model=local_path, device=device)

data = st.text_area("Enter Your Review", "Type Here")
if st.button("Predict"):
    with st.spinner("Predicting........... Please Wait"):
        time.sleep(2)
        result = classifier(data)[0]
        st.write(f"Sentiment: {result['label']}, with score: {result['score']}")