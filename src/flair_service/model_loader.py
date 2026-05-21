import os
from google.cloud import storage
from flair.models import SequenceTagger


GCS_BUCKET = "chat-rfq-ai-data"
GCS_DATA_PREFIX = "training"
LOCAL_MODEL_PATH = "/tmp/final-model.pt"
GCS_MODEL_PATH = "models/flair-rfq/final-model.pt"

def load_model():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)


    blob = bucket.blob(GCS_MODEL_PATH)
    blob.download_to_filename(LOCAL_MODEL_PATH)
    model = SequenceTagger.load(LOCAL_MODEL_PATH)
    return model;