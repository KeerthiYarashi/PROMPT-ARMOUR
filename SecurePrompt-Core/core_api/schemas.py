from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    """Pydantic model for incoming inference requests."""
    prompt: str = Field(..., min_length=1, max_length=2000)

class InferenceResponse(BaseModel):
    """Pydantic model for outputting inference predictions."""
    label: int
    confidence: float
    verdict: str
    action: str = "pass"
    flagged_by: str
    inference_time_ms: float
    tfidf_score: float = 0.0
    distilbert_score: float = 0.0
    context_features: dict = {}
    method: str = "ensemble"

class HealthResponse(BaseModel):
    """Pydantic model for API health check."""
    status: str
    model_loaded: bool
    device: str
    threshold: float

class ExplainRequest(BaseModel):
    """Pydantic model for explanation requests."""
    prompt: str = Field(..., min_length=1, max_length=2000)
    ml_metadata: dict

class ExplainResponse(BaseModel):
    """Pydantic model for explanation response."""
    explanation: str
    attack_type: str
    risk_level: str