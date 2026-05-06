from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from pathlib import Path
from src.ml.dataset import load_corpus
from google.cloud import storage
import os

GCS_BUCKET = "chat-rfq-ai-data"
GCS_DATA_PREFIX = "training"
GCS_MODEL_PREFIX = "models/flair-rfq"

LOCAL_DATA_DIR = Path("/app/data/ner")
LOCAL_MODEL_DIR = Path("/app/model")

USE_GCS = os.getenv("USE_GCS", "true").lower() == "true"

def download_from_gcs():
    print("Downloading data from GCS ...")

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    LOCAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for file in ["train.txt", "dev.txt", "test.txt"]:
        blob = bucket.blob(f"{GCS_DATA_PREFIX}/{file}")
        local_file = LOCAL_DATA_DIR / file

        print(f"Downloading {file} → {local_file}")
        blob.download_to_filename(local_file)

def upload_to_gcs():
    from google.cloud import storage

    print("Uploading model to GCS...")

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)

    for file in LOCAL_MODEL_DIR.glob("*"):
        blob = bucket.blob(f"{GCS_MODEL_PREFIX}/{file.name}")

        print(f"Uploading {file} → gs://{GCS_BUCKET}/{GCS_MODEL_PREFIX}/{file.name}")
        blob.upload_from_filename(file)

def train_model():
    if USE_GCS:
        download_from_gcs()
    else:
        print("Using local data...")

    corpus, tag_dictionary = load_corpus()

    embeddings = StackedEmbeddings([
        WordEmbeddings("glove"),
        FlairEmbeddings("news-forward"),
        FlairEmbeddings("news-backward"),
    ])

    tagger = SequenceTagger(
        hidden_size=256,
        embeddings=embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=True
    )

    trainer = ModelTrainer(tagger, corpus)

    trainer.train(
        base_path=LOCAL_MODEL_DIR,
        learning_rate=0.1,
        mini_batch_size=16,
        max_epochs=10
    )

    if USE_GCS:
        upload_to_gcs()
    else:
        print("Skipping GCS upload (local mode)")


if __name__ == "__main__":
    train_model()