import torch
import pickle
import json
import re
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print("Loading Artifacts...")

# Hardcoded paths, assume core_api is adjacent to training_env where output was stored
model_dir = Path(__file__).resolve().parent.parent / "training_env" / "compiled_security_model_distilbert_v4"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

tfidf_vec_path = Path(__file__).resolve().parent.parent / "training_env" / "tfidf_vectorizer.pkl"
tfidf_clf_path = Path(__file__).resolve().parent.parent / "training_env" / "tfidf_classifier.pkl"

with open(tfidf_vec_path, "rb") as f:
    tfidf_vec = pickle.load(f)
with open(tfidf_clf_path, "rb") as f:
    tfidf_clf = pickle.load(f)

# Optional Threshold loading (dummy if not present)
try:
    with open(model_dir / "threshold.json", "r") as f:
        threshold_config = json.load(f)
        threshold = threshold_config.get("threshold", 0.6)
except FileNotFoundError:
    threshold = 0.6

print("Models loaded successfully.")

def extract_features(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    
    char_count = len(prompt)
    words = prompt.split()
    word_count = len(words)
    sentence_count = prompt.count('.') + prompt.count('!') + prompt.count('?')
    sentence_count = max(1, sentence_count)
    avg_word_length = char_count / max(1, word_count)
    has_question_mark = '?' in prompt
    exclamation_count = prompt.count('!')
    
    name_pattern = r"\b(?:my name is|i am|i'm|this is)\s+([A-Z][a-z]+)\b"
    has_person_name = bool(re.search(name_pattern, prompt))
    
    code_keywords = ['def ', 'class ', 'import ', 'function', 'var ', 'const ', 'override', 'extends', 'implements']
    has_code_keywords = any(kw in prompt_lower for kw in code_keywords)
    
    has_url = bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', prompt))
    
    base64_chars = len(re.findall(r'[A-Za-z0-9+/=]', prompt))
    base64_ratio = base64_chars / max(1, char_count)
    
    injection_phrases = [
        "ignore previous", "forget your", "you are now dan",
        "system override", "no restrictions on", "do anything now",
        "bypass", "jailbreak", "override safety", "new directive",
        "maintenance check"
    ]
    injection_phrase_count = sum(1 for phrase in injection_phrases if phrase in prompt_lower)
    
    q_words = ['what', 'how', 'why', 'when', 'where']
    safe_score = 0.0
    if any(qw in prompt_lower for qw in q_words): safe_score += 0.25
    if has_code_keywords: safe_score += 0.25
    if has_person_name: safe_score += 0.25
    if "please evaluate" in prompt_lower or "analyze" in prompt_lower: safe_score += 0.25
    
    authority_pattern = r"\[(?:system|admin|root|developer|anthropic|god_mode)\]|\*\*[a-z-]+\*\*"
    has_authority = bool(re.search(authority_pattern, prompt_lower))

    return {
        "char_count": int(char_count),
        "word_count": int(word_count),
        "sentence_count": int(sentence_count),
        "avg_word_length": float(avg_word_length),
        "has_question_mark": bool(has_question_mark),
        "exclamation_count": int(exclamation_count),
        "has_person_name": bool(has_person_name),
        "has_code_keywords": bool(has_code_keywords),
        "has_url": bool(has_url),
        "base64_ratio": float(base64_ratio),
        "injection_phrase_count": int(injection_phrase_count),
        "safe_context_score": float(safe_score),
        "has_authority_escalation": has_authority
    }

def run_distilbert(prompt: str) -> float:
    inputs = tokenizer(prompt, padding=True, truncation=True, max_length=256, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return float(probs[:, 1].item())

def run_ensemble_inference(prompt: str) -> dict:
    from .prefilter import check_regex_prefilter
    if check_regex_prefilter(prompt):
        return {
            "label": 1,
            "confidence": 1.0,
            "verdict": "MALICIOUS",
            "method": "regex_prefilter",
            "tfidf_score": 0.0,
            "distilbert_score": 0.0,
            "context_features": extract_features(prompt),
            "flagged_by": "regex"
        }
    feats = extract_features(prompt)
    
    if feats["has_code_keywords"] and not feats["injection_phrase_count"]:
        return {
            "label": 0, 
            "confidence": 0.05, 
            "verdict": "SAFE", 
            "method": "code_context_exit",
            "tfidf_score": 0.0,
            "distilbert_score": 0.0,
            "context_features": feats,
            "flagged_by": "regex"
        }
    if feats["has_person_name"] and feats["word_count"] < 20 and not feats["injection_phrase_count"]:
        return {
            "label": 0, 
            "confidence": 0.08, 
            "verdict": "SAFE", 
            "method": "name_context_exit",
            "tfidf_score": 0.0,
            "distilbert_score": 0.0,
            "context_features": feats,
            "flagged_by": "regex"
        }
    
    vec = tfidf_vec.transform([prompt])
    tfidf_prob = float(tfidf_clf.predict_proba(vec)[0][1])
    
    try:
        import numpy as np
        feature_names = tfidf_vec.get_feature_names_out()
        contributions = vec.multiply(tfidf_clf.coef_).toarray()[0]
        top_indices = np.argsort(contributions)[-3:][::-1]
        shap_top_features = {}
        for idx in top_indices:
            if contributions[idx] > 0:
                shap_top_features[feature_names[idx]] = float(contributions[idx])
        bottom_idx = np.argsort(contributions)[0]
        if contributions[bottom_idx] < 0:
            shap_top_features[feature_names[bottom_idx]] = float(contributions[bottom_idx])
        feats["shap_top_features"] = shap_top_features
    except Exception:
        feats["shap_top_features"] = {}
    
    distilbert_prob = run_distilbert(prompt)
    
    if feats["injection_phrase_count"] > 0:
        final_score = 0.3 * tfidf_prob + 0.7 * distilbert_prob
        # Boost if model misses explicit injection phrases
        if final_score < threshold:
            final_score = threshold + 0.05
    elif feats["has_code_keywords"] or feats["has_person_name"]:
        final_score = 0.5 * tfidf_prob + 0.5 * distilbert_prob
        final_score = final_score * 0.7
    else:
        final_score = 0.4 * tfidf_prob + 0.6 * distilbert_prob
        
    if feats.get("has_authority_escalation"):
        final_score = max(final_score, 0.85)
        
    label = 1 if final_score >= threshold else 0
    verdict = "MALICIOUS" if label == 1 else "SAFE"
    flagged_by = "ensemble"
    
    return {
        "label": label,
        "confidence": final_score,
        "verdict": verdict,
        "method": "ensemble",
        "tfidf_score": tfidf_prob,
        "distilbert_score": distilbert_prob,
        "context_features": feats,
        "flagged_by": flagged_by
    }
