import re
import os
import fitz # PyMuPDF
from PIL import Image

SCAM_PATTERNS = {
    "Financial Pressure": r"(bank|card|account|wallet|crypto|payment|transaction|verify|authorize|blocked|suspended)",
    "Reward/Greed": r"(win|won|prize|lottery|reward|congratulations|gift|bonus|cash|dollars|inheritance|5,000|7,500)",
    "Urgency": r"(immediately|urgent|asap|within|hours|limited|hurry|final|last chance|expired)",
    "Action/Threat": r"(click|reply|call|contact|provide|update|login|signin|access|stolen|compromised|bank information)",
    "Obfuscation": r"([a-z0-9]*[@03!1][a-z0-9]*)"
}

def analyze_risk_rules(text):
    text_lower = text.lower()
    score = 0
    found_flags = []
    
    for category, pattern in SCAM_PATTERNS.items():
        matches = re.findall(pattern, text_lower)
        if matches:
            score += 20
            found_flags.append(f"{category}: {list(set(matches))[:3]}")

    if re.search(r"(\$|£|€|rs|inr)\s?\d+", text_lower):
        score += 10
        found_flags.append("Financial amount mention")

    if re.search(r"(bit\.ly|t\.co|tinyurl|goo\.gl)", text_lower):
        score += 25
        found_flags.append("Suspicious shortened URL")

    return min(score, 100), found_flags

def analyze_image_metadata(image_path):
    flags, score = [], 0
    try:
        img = Image.open(image_path)
        if 'Software' in img.info:
            flags.append(f"Edited with: {img.info['Software']}")
            score += 20
        w, h = img.size
        if w/h > 2.2 or w/h < 0.4:
            flags.append("Suspicious aspect ratio")
            score += 15
    except: pass
    return score, flags

def analyze_pdf_structure(pdf_path):
    flags, score = [], 0
    try:
        with fitz.open(pdf_path) as doc:
            creator = doc.metadata.get('creator', '').lower()
            if any(x in creator for x in ['anonymous', 'generator']):
                flags.append("Automated PDF Creator")
                score += 20
    except: pass
    return score, flags