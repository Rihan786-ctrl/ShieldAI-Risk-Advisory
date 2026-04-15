import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Models', 'distilbert_scam_Model')
REMOTE_MODEL_NAME = "prithivMLmods/Spam-Bert-Uncased"


def load_model():
    if os.path.isdir(MODEL_PATH):
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            return tokenizer, model
        except Exception as e:
            print(f"Error loading local model from {MODEL_PATH}: {e}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(REMOTE_MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(REMOTE_MODEL_NAME)
        print(f"Loaded remote model: {REMOTE_MODEL_NAME}")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading remote model {REMOTE_MODEL_NAME}: {e}")
        return None, None


tokenizer, model = load_model()


def get_detailed_ai_metrics(text):
    if not text or tokenizer is None or model is None:
        return {
            "risk_score": 10,
            "scam_prob": 0.1,
            "raw_logits": [2.0, -2.0]
        }

    inputs = tokenizer(text[:512], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits[0].cpu().numpy()
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0].cpu().numpy()

    return {
        "risk_score": int(probs[1] * 100),
        "raw_logits": [float(logits[0]), float(logits[1])],
        "scam_prob": float(probs[1])
    }
