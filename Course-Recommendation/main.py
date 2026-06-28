"""
FastAPI entry point.
Start with: uvicorn main:app --reload
"""

import logging
import re

import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from sentence_transformers import SentenceTransformer

from config import (
    MODEL_PATH,
    DATASET_PATH,
    EMBEDDINGS_PATH,
    COURSE_INDEX_PATH,
    FLAT_SKILLS_PATH,
    DEFAULT_TOP_K,
)
from recommend import recommend_courses

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# Holds all heavy state loaded at startup
_state: dict = {}

VALID_EXPERIENCE_LEVELS = {"beginner", "intermediate", "advanced"}


def _parse_skills(raw: str) -> list[str]:
    parts = re.split(r"\s{2,}", str(raw).strip())
    return [p.strip() for p in parts if p.strip()]


def _load_app_state() -> None:
    """Load model, dataset, and embeddings into _state. Called once at startup."""

    log.info("Loading model from %s", MODEL_PATH)
    _state["model"] = SentenceTransformer(str(MODEL_PATH))

    log.info("Loading dataset from %s", DATASET_PATH)
    df = pd.read_csv(DATASET_PATH, encoding="utf-8", encoding_errors="replace")
    df = df.dropna(subset=["Skills", "Course Name", "Difficulty Level"]).reset_index(drop=True)
    df["skills_list"] = df["Skills"].apply(_parse_skills)
    _state["df"] = df
    log.info("Loaded %d courses.", len(df))

    log.info("Loading cached embeddings...")
    _state["skill_embeddings"] = np.load(EMBEDDINGS_PATH)
    _state["flat_course_idx"]  = np.load(COURSE_INDEX_PATH)
    _state["flat_skills"]      = np.load(FLAT_SKILLS_PATH, allow_pickle=True)
    log.info("Loaded %d skill embeddings.", len(_state["flat_skills"]))


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_app_state()
    yield
    _state.clear()
    log.info("App state cleared on shutdown.")


app = FastAPI(
    title="Course Recommendation API",
    description="Recommends Coursera courses based on skill gaps and experience level.",
    version="1.0.0",
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# Schema
# ------------------------------------------------------------------

class RecommendRequest(BaseModel):
    missing_skills:    list[str] = Field(..., min_length=1)
    experience_level:  str       = Field(..., examples=["beginner", "intermediate", "advanced"])
    top_k:             int       = Field(DEFAULT_TOP_K, ge=1, le=20)
    courses_per_skill: int       = Field(5, ge=1, le=5)

    @field_validator("experience_level")
    @classmethod
    def validate_experience(cls, v: str) -> str:
        if v.lower() not in VALID_EXPERIENCE_LEVELS:
            raise ValueError(f"experience_level must be one of {VALID_EXPERIENCE_LEVELS}")
        return v.lower()

    @field_validator("missing_skills")
    @classmethod
    def validate_skills(cls, v: list[str]) -> list[str]:
        cleaned = [s.strip() for s in v if s.strip()]
        if not cleaned:
            raise ValueError("missing_skills must contain at least one non-empty string.")
        return cleaned


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "courses_loaded": len(_state.get("df", []))}


@app.post("/recommend")
def recommend(request: RecommendRequest):
    if not _state:
        raise HTTPException(status_code=503, detail="Model not ready.")

    results = recommend_courses(
        model=_state["model"],
        df=_state["df"],
        skill_embeddings=_state["skill_embeddings"],
        flat_skills=_state["flat_skills"],
        flat_course_idx=_state["flat_course_idx"],
        missing_skills=request.missing_skills,
        experience_level=request.experience_level,
        top_k=request.top_k,
        courses_per_skill=request.courses_per_skill,
    )

    return {"recommendations": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)