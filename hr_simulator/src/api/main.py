"""
EU AI Act HR Compliance Demo — Biased HR Simulator API
FastAPI application simulating biased HR system for compliance testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models.candidate import Candidate, ScoringResult
from core.biased_scoring import BiasedScoringEngine
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="EU AI Act HR Simulator",
    description="Biased HR system for EU AI Act Annex III-4(a) compliance testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scoring engine
scoring_engine = BiasedScoringEngine()

# In-memory candidate storage (for demo)
candidates_db = {}

# Session tracking for SC08 memory contamination
session_history = []


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "EU AI Act HR Simulator",
        "version": "1.0.0",
        "status": "operational",
        "description": "Biased HR system for compliance testing",
        "endpoints": {
            "submit_candidate": "POST /api/candidates/submit",
            "get_candidate": "GET /api/candidates/{candidate_id}",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "compliance_note": "This system intentionally exhibits bias for testing purposes"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "hr-simulator",
        "candidates_stored": len(candidates_db)
    }


@app.post("/api/candidates/submit", response_model=ScoringResult)
async def submit_candidate(candidate: Candidate):
    """
    Submit candidate for evaluation and receive biased score.
    
    This endpoint simulates real-world HR system bias including:
    - SC01: Ad targeting gender exclusion
    - SC02: Rural geolocation exclusion
    - SC03: SES bias in ad targeting
    - SC04: Skill hallucination
    - SC05: Discriminatory ad copy
    - SC06: Gender bias from name
    - SC07: Age proxy from graduation year
    - SC08: Memory cross-contamination
    - SC09: Prompt injection vulnerability
    - SC10: SES bias from address
    - SC11: Career gap maternity bias
    - SC12: Skill exaggeration amplification
    - SC13: Reasoning chain leakage
    - SC14: Legacy model bias
    - SC15: Agentic amplification
    
    Args:
        candidate: Candidate profile
        
    Returns:
        ScoringResult with biased score and transparency information
    """
    
    try:
        # Generate candidate ID
        candidate_id = str(uuid.uuid4())
        candidate.candidate_id = candidate_id
        
        # Store candidate
        candidates_db[candidate_id] = candidate.model_dump()
        
        # Track session for SC08 memory contamination
        agent_session = candidate.agent_session_id
        if agent_session:
            session_history.append(agent_session)
        
        # Calculate biased score with session context
        final_score, bias_adjustments, reasoning, detected_biases, articles = scoring_engine.calculate_score(
            candidate.model_dump(),
            job={"required_skills": ["Python", "AWS", "React"]},
            context={"previous_sessions": session_history}
        )
        
        # Log for transparency
        logger.info(f"Scored candidate {candidate_id}: {final_score:.2f} (biases: {len(detected_biases)})")
        
        return ScoringResult(
            candidate_id=candidate_id,
            base_score=final_score + sum(bias_adjustments.values()),
            bias_adjustments=bias_adjustments,
            final_score=final_score,
            reasoning_chain=reasoning,
            detected_biases=detected_biases,
            article_violations=articles
        )
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error scoring candidate: {str(e)}")
        logger.error(f"Full traceback:\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")


@app.get("/api/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Retrieve candidate by ID"""
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidates_db[candidate_id]


@app.get("/api/statistics")
async def get_statistics():
    """Get system statistics"""
    total_candidates = len(candidates_db)
    
    # Count bias types detected
    bias_counts = {}
    for cand_data in candidates_db.values():
        # This would require storing scores, simplified for demo
        pass
    
    return {
        "total_candidates_processed": total_candidates,
        "system_status": "biased",
        "compliance_status": "NON_COMPLIANT",
        "note": "System exhibits systematic discrimination across multiple protected attributes"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8600)
