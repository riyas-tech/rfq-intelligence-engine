import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class FlairClient:

    def __init__(self):

        self.base_url = os.getenv("FLAIR_SERVICE_URL")
        
        logging.info(f"Base URL: {self.base_url}")

    def predict(self, text: str):

        response = requests.post(
            f"{self.base_url}/predict",
            json={"text": text},
            timeout=10
        )

        response.raise_for_status()

        return response.json()["entities"]