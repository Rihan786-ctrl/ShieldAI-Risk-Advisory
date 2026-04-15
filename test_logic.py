from scripts.aggregator import calculate_final_risk

msg = "Your Netflix account is on hold. Update payment info here: http://bit.ly/fake-link"
result = calculate_final_risk(msg)

print(f"Final Risk Score: {result['score']}%")
print(f"Risk Level: {result['level']}")
print(f"AI Confidence: {result['ai_confidence']}%")