from vertexai.generative_models import GenerativeModel
import json

class LLMClient:
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-pro")
    def extract_trade(self, text:str):
        prompt = f"""
            You are a trading assistant.
            Extact structured RFQ information from the message.
            Return ONLY valid JSON:

{{
  "intent": "RFQ | TRADE | QUERY",
  "pair": "string or null",
  "notional": number or null,
  "tenor": "string or null",
  "side": "BUY | SELL | RFQ | null"
}}

Message:
{text}
        """

        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return None    