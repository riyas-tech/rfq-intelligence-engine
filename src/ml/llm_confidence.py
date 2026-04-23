def calculate_llm_confidence(result: dict):
    if not result:
        return 0.0
    
    score = 0.0

    if result.get("pair"):
        score+= 0.3

    if result.get("notional"):
        score += 0.3

    if result.get("tenure"):
        score += 0.2

    if result.get("intent"):
        score += 0.2

    return score

                
