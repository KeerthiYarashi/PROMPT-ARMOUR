import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .model_loader import load_all_artifacts
from .ensemble_inference import run_ensemble_inference
from .schemas import PromptRequest, InferenceResponse, HealthResponse
from .config import DEVICE, THRESHOLD, API_RATE_LIMIT
from .middleware import limiter, LoggingAndLengthMiddleware, logger as mw_logger

# Use existing configured logger
logger = logging.getLogger("api_request_logger")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load artifacts on startup (triggers log message and prevents per-request cold start)
    load_all_artifacts()
    yield

app = FastAPI(
    title="SecurePrompt API",
    version="2.0.0",
    description="Production-grade ML API for Prompt Injection Detection",
    lifespan=lifespan
)

# Attach rate limiter and handlers
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Attach Middlewares
# CRITICAL: CORSMiddleware must be added BEFORE other middlewares and rate limiters
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(LoggingAndLengthMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler returns clean JSON 500s."""
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "status": 500}
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    artifacts = load_all_artifacts()
    return HealthResponse(
        status="healthy",
        model_loaded=artifacts["model"] is not None,
        device=str(DEVICE),
        threshold=THRESHOLD
    )

@app.get("/model-info")
async def get_model_info():
    return {
        "distilbert_version": "v4",
        "ensemble": True,
        "components": ["regex", "tfidf", "distilbert"],
        "threshold": THRESHOLD,
        "hard_negatives_trained": 1
    }

@app.post("/analyze", response_model=InferenceResponse)
@limiter.limit(API_RATE_LIMIT)
async def analyze_prompt(request: Request, body: PromptRequest):
    """Analyze a prompt for malicious intent."""
    import time
    start = time.perf_counter()
    result = run_ensemble_inference(body.prompt)
    latency_ms = (time.perf_counter() - start) * 1000.0
    result["inference_time_ms"] = latency_ms
    
    # Log specific inference details
    logger.info(
        f"Prompt: {body.prompt[:50]}... | "
        f"Verdict: {result['verdict']} | "
        f"Conf: {result['confidence']:.3f} | "
        f"Latency: {result['inference_time_ms']:.2f}ms"
    )
    
    return InferenceResponse(**result)