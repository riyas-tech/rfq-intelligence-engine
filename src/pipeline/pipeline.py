from src.preprocessing.cleaner import clean_text
from src.rules.extractor import extract_trade


def process_message(message: str):
    cleaned = clean_text(message)
    trade = extract_trade(cleaned)
    return trade