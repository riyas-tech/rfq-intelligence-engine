from flair.models import SequenceTagger
from flair.data import Sentence
from pathlib import Path

class FlairPredictor:
    def __init__(self, model_path = "models/flair-rfq/final-model.pt"):
        model_path = Path("models/flair-rfq/final-model.pt").resolve()
        model_path_str = model_path.as_posix()
        self.model = SequenceTagger.load(model_path_str)

    def predict(self, text: str):
        sentence = Sentence(text)
        self.model.predict(sentence)

        entitites = []

        for entity in sentence.get_spans("ner"):
            entitites.append({
                "text" : entity.text,
                "label" : entity.tag,
                "confidence": float(entity.score)
            })    

        return entitites

