from flask import Flask, request, jsonify
from src.pipeline.pipeline import process_message
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/health")
def health():
    return {"status" : "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    if not payload or "message" not in payload:
        return jsonify({
            "error" : "message field required"
        }), 400

    message = payload["message"]
    try:
        trade = process_message(message)

        return jsonify(
            trade.model_dump()
        )
    
    except Exception as e:
        return jsonify({
            "error" : str(e)
        }), 500
    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )    
