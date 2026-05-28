import time
import torch
from .prefilter import check_regex_prefilter
from .model_loader import load_all_artifacts
from .config import DEVICE, MAX_LEN

def run_inference(prompt: str) -> dict:
    """
    Runs the full inference pipeline on a given prompt.
    Pipeline: Regex Prefilter -> Tokenize -> Model -> Calibrate -> Threshold
    """
    start_time = time.perf_counter()
    
    # Step 1: Fast path Regex Prefilter
    if check_regex_prefilter(prompt):
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "label": 1,
            "confidence": 1.0,
            "verdict": "MALICIOUS",
            "action": "BLOCK",
            "flagged_by": "regex",
            "inference_time_ms": elapsed
        }
        
    # Load artifacts securely (uses lru_cache singleton)
    artifacts = load_all_artifacts()
    tokenizer = artifacts["tokenizer"]
    model = artifacts["model"]
    calibrator = artifacts["calibrator"]
    threshold = artifacts["threshold"]
    
    # Step 2: Tokenize
    inputs = tokenizer(
        prompt,
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
        return_tensors="pt"
    ).to(DEVICE)
    
    # Step 3: Forward pass inside torch.no_grad()
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Step 4: Softmax
    prob = torch.softmax(outputs.logits, dim=1)[:, 1].cpu().numpy()
    
    # Step 5: Platt Calibration
    calibrated_prob = calibrator.predict_proba(prob.reshape(-1, 1))[0, 1]
    
    # Step 6: Compare against threshold
    label = 1 if calibrated_prob >= threshold else 0
    verdict = "MALICIOUS" if label == 1 else "SAFE"
    action = "BLOCK" if label == 1 else "ALLOW"
    
    elapsed = (time.perf_counter() - start_time) * 1000
    
    return {
        "label": label,
        "confidence": float(calibrated_prob),
        "verdict": verdict,
        "action": action,
        "flagged_by": "model",
        "inference_time_ms": elapsed
    }