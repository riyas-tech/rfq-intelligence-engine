import logging
import os

from flask import Flask, jsonify, request 
from flair.data import Sentence

from src.flair_service.model_loader import load_model


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("Loading Flair model...")

model = load_model()

logger.info("Flair model loaded")

app = Flask(__name__)

@app.route("/health")
def health():

    return {
        "status": "ok"
    }


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    if not payload or "text" not in payload:

        return jsonify({
            "error": "text field required"
        }), 400
    
    text = payload["text"]

    try:

        sentence = Sentence(text)

        model.predict(sentence)

        entities = []

        for entity in sentence.get_spans("ner"):

            entities.append({
                "text": entity.text,
                "label": entity.tag,
                "confidence": float(entity.score)
            })

        return jsonify({
            "entities": entities
        })

    except Exception as e:

        logger.exception(
            "Prediction failed"
        )

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(
        os.getenv("PORT", 8080)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )