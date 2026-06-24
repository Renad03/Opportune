"""
Job Recommender API
FastAPI wrapper for the HGT-based job recommendation model.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from contextlib import asynccontextmanager
import torch
import torch.nn.functional as F
from collections import defaultdict
import logging

from model import HGTModel, Predictor
from graph import build_graph
from recommend import recommend_jobs
from config import Settings

# ─── Logging ────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

# ─── Global state (loaded once at startup) ──────────────────────────────────

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model and graph on startup; clean up on shutdown."""
    logger.info("Loading graph from Neo4j …")
    hetero_graph, in_channels_dict, encoder = build_graph(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )

    logger.info("Loading model weights …")
    checkpoint = torch.load(settings.checkpoint_path, map_location=settings.device, weights_only=False)
    model = HGTModel(
        metadata=hetero_graph.metadata(),
        in_channels_dict=in_channels_dict,
        hidden=settings.hidden_dim,
        num_layers=settings.num_layers,
        dropout=settings.dropout,
    ).to(settings.device)

    predictor = Predictor(
        dim=checkpoint["embed_dim"],
        dropout=settings.dropout,
    ).to(settings.device)

    model.load_state_dict(checkpoint["model_state_dict"])
    predictor.load_state_dict(checkpoint["predictor_state_dict"])
    model.eval()
    predictor.eval()

    state["model"] = model
    state["predictor"] = predictor
    state["graph"] = hetero_graph
    state["encoder"] = encoder
    state["device"] = settings.device

    logger.info("✅ API ready.")
    yield

    state.clear()
    logger.info("Shutdown complete.")


# ─── App ────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Job Recommender API",
    description="HGT-based job recommendation using skills & experience level.",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Schemas ────────────────────────────────────────────────────────────────

EXPERIENCE_LEVELS = ["intern", "fresher", "junior", "mid", "senior", "lead", "unspecified"]


class RecommendRequest(BaseModel):
    skills: List[str] = Field(
        ...,
        min_length=1,
        description="List of the user's skills.",
        examples=[["Python", "Docker", "FastAPI", "AWS"]],
    )
    experience: str = Field(
        default="mid",
        description=f"Experience level. One of: {EXPERIENCE_LEVELS}",
        examples=["senior"],
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of job recommendations to return.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "skills": ["Python", "Docker", "FastAPI", "AWS", "Pandas"],
                "experience": "senior",
                "top_k": 5,
            }
        }
    }


class JobRecommendation(BaseModel):
    job_title: str
    recommended_skills: List[str]
    contributing_skills: List[str]
    final_score: float


class RecommendResponse(BaseModel):
    recommendations: List[JobRecommendation]
    matched_skills: List[str]
    unmatched_skills: List[str]


# ─── Routes ─────────────────────────────────────────────────────────────────


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/skills", tags=["meta"])
def list_skills():
    """Return all skills currently in the graph."""
    graph = state.get("graph")
    if graph is None:
        raise HTTPException(503, "Model not loaded yet.")
    return {"skills": sorted(graph["Skill"].text)}


@app.get("/experience-levels", tags=["meta"])
def list_experience_levels():
    return {"experience_levels": EXPERIENCE_LEVELS}


@app.post("/recommend", response_model=RecommendResponse, tags=["recommend"])
def recommend(req: RecommendRequest):
    """
    Return top-K job recommendations for a user given their skills and experience level.
    """
    if req.experience.lower() not in EXPERIENCE_LEVELS:
        raise HTTPException(
            400,
            f"Invalid experience level '{req.experience}'. "
            f"Choose from: {EXPERIENCE_LEVELS}",
        )

    graph = state["graph"]

    # Track which skills matched
    skill_texts_lower = [s.lower() for s in graph["Skill"].text]
    matched = [s for s in req.skills if s.lower() in skill_texts_lower]
    unmatched = [s for s in req.skills if s.lower() not in skill_texts_lower]

    if not matched:
        raise HTTPException(
            422,
            detail={
                "message": "None of the provided skills exist in the graph.",
                "unmatched_skills": unmatched,
                "hint": "Call GET /skills to see available skills.",
            },
        )

    jobs = recommend_jobs(
        user_skills=req.skills,
        user_experience=req.experience,
        model=state["model"],
        predictor=state["predictor"],
        graph=graph,
        encoder=state["encoder"],
        top_k=req.top_k,
        device=state["device"],
    )

    return RecommendResponse(
        recommendations=[JobRecommendation(**j) for j in jobs],
        matched_skills=matched,
        unmatched_skills=unmatched,
    )