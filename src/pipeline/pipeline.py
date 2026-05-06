from src.preprocessing.cleaner import clean_text
from src.rules.extractor import extract_trade
from src.ml.predictor import FlairPredictor
from src.ml.llm_client import LLMClient
from src.ml.llm_confidence import calculate_llm_confidence


predictor = FlairPredictor()
llm = LLMClient()

def compute_ml_confidence(entities):
    if not entities:
        return 0.0
    
    weights = {
        "PAIR" : 0.3,
        "NOTIONAL" : 0.3,
        "TENOR" : 0.2,
        "SIDE"  : 0.2
    }

    score = 0.0
    for ent in entities:
        label = ent["label"].replace("B-", "").replace("I-", "")
        weight = weights.get(label, 0)
        score += ent["confidence"] * weight

    return score 




def merge_results(base_trade, ml_entities):
    # fallback strategy: ML overrides missing rule fields
    trade = base_trade 

    for ent in ml_entities:
        if ent["label"] == "B-PAIR" and not trade.pair:
            trade.pair = ent["text"].upper()

        if ent["label"] == "B-NOTIONAL" and not trade.notional:
            value = ent["text"].lower().replace("m", "")
            trade.notional = float(value) * 1_000_000

        if ent["label"] == "B-TENOR" and not trade.tenor:
            trade.tenor = ent["text"].upper()

    # if llm_result:
    #     if not trade.pair:
    #         trade.pair = llm_result.get("pair")

    #     if not trade.notional:
    #         trade.notional = llm_result.get("notional")

    #     if not trade.tenor:
    #         trade.tenor = llm_result.get("tenor")

    #     if not trade.side:
    #         trade.side = llm_result.get("side")    

    return trade

def process_message(message: str):
    cleaned = clean_text(message)

    # 1. Rule Layer 
    rule_trade = extract_trade(cleaned)
    rule_conf = rule_trade.confidence

    # 2. ML layer
    ml_entities = predictor.predict(cleaned)
    ml_conf = compute_ml_confidence(ml_entities)

     # 3. LLM fallback (ONLY if low confidence)
    llm_result = None
    llm_conf = 0.0

    if rule_conf >= 0.85:
        base_trade = rule_trade
        source = "RULE"

    # elif ml_conf >= 0.85:
    else:
        base_trade = ml_entities
        source = "FLAIR"

    # else:
    #     llm_result = llm.extract_trade(cleaned)
    #     llm_conf = calculate_llm_confidence(llm_result)

        base_trade = rule_trade
        # source = "LLM"

    final_trade = merge_results(base_trade, ml_entities)

    final_trade.confidence = max(rule_conf, ml_conf)
    final_trade.source = source

    return final_trade