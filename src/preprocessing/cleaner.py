import re

def clean_text(text: str) -> str:
    text = text.lower().strip()

    # Expand common abbreviations
    text = re.sub(r"\b(\d+)m\b", r"\1 million", text)
    text = re.sub(r"\btmr\b", "tomorrow", text)

    # fix split pairs
    text = re.sub(r"\b([a-z]{3})/([a-z]{3})\b", r"\1 \2", text)

    # normalize slang
    text = text.replace("px", "price")
    
    return text