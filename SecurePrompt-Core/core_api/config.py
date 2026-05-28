import os
import json
import torch
from pathlib import Path

# Paths relative to core_api directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "training_env" / "compiled_security_model_distilbert_v2"
THRESHOLD_PATH = MODEL_DIR / "threshold.json"
CALIBRATOR_PATH = MODEL_DIR / "calibrator.pkl"

MAX_LEN = 256
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
API_RATE_LIMIT = "100/minute"

def get_threshold() -> float:
    """Loads the optimal threshold from the json file."""
    if THRESHOLD_PATH.exists():
        with open(THRESHOLD_PATH, "r") as f:
            data = json.load(f)
            return float(data.get("optimal_threshold", 0.5))
    return 0.5

THRESHOLD = get_threshold()