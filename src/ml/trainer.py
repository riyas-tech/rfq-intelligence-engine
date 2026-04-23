from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from pathlib import Path
from src.ml.dataset import load_corpus


def train_model():
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
        base_path="models/flair-rfq",
        learning_rate=0.1,
        mini_batch_size=16,
        max_epochs=10
    )

if __name__ == "__main__":
    train_model()