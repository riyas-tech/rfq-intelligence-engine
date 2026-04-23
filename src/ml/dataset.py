from flair.datasets import ColumnCorpus
from pathlib import Path
# Columncorpus : dataset designed to load data where each token and its corresponding label are in separate columns


def load_corpus():
    columns = {0: "text", 1: "ner"}
    data_folder = Path("data/ner")
    print("Resolved path :", data_folder.resolve())
    print("Train path   :", data_folder/"train.txt")
    print("Train exists", (data_folder/"train.txt").exists())

    corpus = ColumnCorpus(
        data_folder,
        column_format=columns,
        train_file="train.txt",
        dev_file="dev.txt",
        test_file="test.txt"
    )

    tag_type = "ner"
    tag_dictionery = corpus.make_label_dictionary(label_type=tag_type)
    return corpus, tag_dictionery