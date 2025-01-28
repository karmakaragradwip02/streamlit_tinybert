import warnings
import streamlit as st
from PIL import Image
import os
from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
import boto3

# Initialize S3 client
s3 = boto3.client('s3')

bucket_name = "tinybertaws"
warnings.filterwarnings("ignore")

# Local path to store downloaded model files
local_path = 'DEPLOY_MODEL_STREAMLIT/downloads/vit-human-pose-classification'
s3_prefix = 'mlmodel-aws/vit-human-pose-classification/'

# Function to download model files from S3
def download_folder(local_path, s3_prefix, bucket_name):
    os.makedirs(local_path, exist_ok=True)
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
        if 'Contents' in result:
            for Key in result['Contents']:
                s3_key = Key['Key']
                if not s3_key.endswith("/"):  # Skip folders
                    local_file = os.path.join(local_path, os.path.relpath(s3_key, s3_prefix))
                    os.makedirs(os.path.dirname(local_file), exist_ok=True)
                    s3.download_file(bucket_name, s3_key, local_file)

# Streamlit app UI
st.title("Machine Learning Model Deployment at the Server!")
button = st.button("Download Model")

if button:
    with st.spinner("Downloading model from S3... Please wait"):
        download_folder(local_path, s3_prefix, bucket_name)
        st.success("Model downloaded successfully!")

st.markdown("## Upload an image to classify the human pose.")
uploaded_file = st.file_uploader(
    "Ensure your external device (e.g., phone or camera) is connected and accessible as a file source.", 
    type=["png", "jpg", "jpeg"]
)

# Check if the model files exist
model_files_exist = os.path.exists(os.path.join(local_path, "pytorch_model.bin")) and os.path.exists(
    os.path.join(local_path, "config.json")
)

image_processor = AutoImageProcessor.from_pretrained(local_path)
model = AutoModelForImageClassification.from_pretrained(local_path)
pipe = pipeline("image-classification", model=model, image_processor=image_processor)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.success("Image successfully uploaded!")

    predict_button = st.button("Predict")

    if predict_button:
        with st.spinner("Predicting... Please wait"):
            try:
                # Perform prediction
                result = pipe(image)
                label = result[0]['label']
                score = result[0]['score']
                st.markdown(f"### Prediction: {label}")
                st.markdown(f"### Confidence Score: {score:.4f}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")
else:
    st.info("Please connect your device and upload an image.")