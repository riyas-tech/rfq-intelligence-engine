from flask import Flask, request, jsonify
from src.pipeline.pipeline import process_message

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    message = data.get("message")
    result = process_message(message)
    return jsonify(result.model_dump())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)