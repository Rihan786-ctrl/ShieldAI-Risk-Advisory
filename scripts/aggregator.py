from scripts.rules import analyze_risk_rules
from scripts.model_inference import get_detailed_ai_metrics # Use the new function

def calculate_final_risk(text):
    # 1. Fetch AI results
    ai_res = get_detailed_ai_metrics(text)
    ai_score = ai_res['risk_score']
    
    # 2. Fetch Heuristic results
    rule_score, flags = analyze_risk_rules(text)
    
    # --- ENSEMBLE LOGIC (The Accuracy Secret) ---
    # If rules find a specific "Critical" pattern, we use the MAX score, 
    # not the average. This prevents AI noise from lowering the risk.
    if rule_score >= 40:
        # High confidence in rules (matches won, bank, lottery, etc.)
        final_score = max(ai_score, rule_score)
    else:
        # Standard hybrid weighting
        final_score = (ai_score * 0.6) + (rule_score * 0.4)
        
    # Final clamping
    final_score = min(int(final_score), 100)
    
    # Determine Label
    if final_score < 30: level = "Low"
    elif final_score < 60: level = "Medium"
    elif final_score < 85: level = "High"
    else: level = "Critical"
    
    return {
        "score": final_score,
        "level": level,
        "flags": flags,
        "ai_metrics": ai_res
    }