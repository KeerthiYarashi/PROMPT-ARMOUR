import joblib
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .config import MODEL_DIR, CALIBRATOR_PATH, DEVICE, THRESHOLD

@lru_cache(maxsize=1)
def load_all_artifacts() -> dict:
    """
    Loads all required artifacts for inference.
    Returns a singleton dictionary to prevent memory leaks and ensure ONCE-only loading.
    """
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Model directory not found at {MODEL_DIR}")
        
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
    model.to(DEVICE)
    model.eval()
    
    calibrator = joblib.load(str(CALIBRATOR_PATH))
    
    print(f"Model loaded successfully on {DEVICE}")
    
    return {
        "model": model,
        "tokenizer": tokenizer,
        "calibrator": calibrator,
        "threshold": THRESHOLD
    }