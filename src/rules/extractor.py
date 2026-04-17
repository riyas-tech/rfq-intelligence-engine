import re
from src.models.trade import Trade

PAIR_PATTERN = r"\b([a-z]{6})\b"
SPLIT_PAIR_PATTERN = r"\b([a-z]{3})\s?([a-z]{3})\b"
NOTIONAL_PATTERN = r"\b(\d+)\s?(million|m)\b"

# --- FX Aliases ---
FX_ALIASES = {
    "cable": "GBPUSD",
    "fiber": "EURUSD",
    "yen": "USDJPY"
}

# --- Intent Keywords ---
RFQ_KEYWORDS = ["quote", "price", "px", "rate"]
TRADE_KEYWORDS = ["buy", "sell"]
QUERY_KEYWORDS = ["what", "show", "check"]

def extract_pair(text: str):
    match = re.search(PAIR_PATTERN, text)
    if match:
        return match.group(1).upper()

    # split pair (eur usd)
    match = re.search(SPLIT_PAIR_PATTERN, text)
    if match:
        return (match.group(1) + match.group(2)).upper()

    for key, value in FX_ALIASES.items():
        if key in text:
            return value

    return None

def extract_notional(text: str):
    match = re.search(NOTIONAL_PATTERN, text)
    if match:
        value = int(match.group(1))
        return value * 1_000_000
    return None

def extract_tenor(text: str):
    if "spot" in text:
        return "SPOT"
    if "tomorrow" in text:
        return "TOMORROW"
    if "next week" in text:
        return "NEXT_WEEK"    
    return None

# Intent detection
def detect_intent(text: str):
    for word in RFQ_KEYWORDS:
        if word in text:
            return "RFQ"

    for word in TRADE_KEYWORDS:
        if word in text:
            return "TRADE"

    for word in QUERY_KEYWORDS:
        if word in text:
            return "QUERY"

    return "UNKNOWN"                        


def calculate_confidence(pair, notional, tenor, intent):
    score = 0.0
    if pair:
        score += 0.3
    if notional:
        score += 0.3
    if tenor:
        score += 0.2
    if intent != "UNKNOWN":
        score += 0.2    
    return score  

def extract_trade(text: str) -> Trade:
    pair = extract_pair(text)
    notional = extract_notional(text)
    tenor = extract_tenor(text)
    intent = detect_intent(text)
    confidence = calculate_confidence(pair, notional, tenor, intent)

    return Trade(
        pair=pair,
        notional=notional,
        tenor=tenor,
        side=intent,
        confidence=confidence,
        source="RULE"
    )