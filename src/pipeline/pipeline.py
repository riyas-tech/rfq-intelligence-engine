from src.preprocessing.cleaner import clean_text
from src.rules.extractor import extract_trade
from src.ml.predictor import FlairPredictor
from src.ml.llm_client import LLMClient
from src.ml.llm_confidence import calculate_llm_confidence


predictor = FlairPredictor()
llm = LLMClient()

def merge_results(rule_trade, ml_entities, llm_result, llm_conf):
    # fallback strategy: ML overrides missing rule fields

    for ent in ml_entities:
        if ent["label"] == "B-PAIR" and not rule_trade.pair:
            rule_trade.pair = ent["text"].upper()

        if ent["label"] == "B-NOTIONAL" and not rule_trade.notional:
            value = ent["text"].lower().replace("m", "")
            rule_trade.notional = float(value) * 1_000_000

        if ent["label"] == "B-TENOR" and not rule_trade.tenor:
            rule_trade.tenor = ent["text"].upper()

    if llm_result:
        if not rule_trade.pair:
            rule_trade.pair = llm_result.get("pair")

        if not rule_trade.notional:
            rule_trade.notional = llm_result.get("notional")

        if not rule_trade.tenor:
            rule_trade.tenor = llm_result.get("tenor")

        if not rule_trade.side:
            rule_trade.side = llm_result.get("side")    

    # ML confidence impact
    ml_conf = sum(e["confidence"] for e in ml_entities) / len(ml_entities) if ml_entities else 0

    rule_trade.confidence = max(
        rule_trade.confidence,
        ml_conf,
        llm_conf
    )

    rule_trade.source = "RULE+FLAIR+LLM"

    return rule_trade

def process_message(message: str):
    cleaned = clean_text(message)

    # 1. Rule Layer 
    rule_trade = extract_trade(cleaned)
    rule_conf = rule_trade.confidence

    # 2. ML layer
    ml_entities = predictor.predict(cleaned)
    ml_conf = calculate_llm_confidence(ml_entities)

     # 3. LLM fallback (ONLY if low confidence)
    llm_result = None
    llm_conf = 0.0
    if rule_trade.confidence < 0.7:
        llm_result = llm.extract_trade(cleaned)
        llm_conf = calculate_llm_confidence(llm_result)

    final_trade = merge_results(rule_trade, ml_entities, llm_result, llm_conf)
    return final_trade