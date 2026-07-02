"""
Offline script — run once to build and cache skill embeddings.
Usage: python build_embeddings.py
"""

import re
import logging

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import (
    MODEL_PATH,
    DATASET_PATH,
    EMBEDDINGS_PATH,
    COURSE_INDEX_PATH,
    FLAT_SKILLS_PATH,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def parse_skills(raw: str) -> list[str]:
    parts = re.split(r"\s{2,}", str(raw).strip())
    return [p.strip() for p in parts if p.strip()]


def main() -> None:
    # ------------------------------------------------------------------
    # Load dataset
    # ------------------------------------------------------------------
    log.info("Loading dataset from %s", DATASET_PATH)

    df = pd.read_csv(DATASET_PATH, encoding="utf-8", encoding_errors="replace")
    df = df.dropna(subset=["Skills", "Course Name", "Difficulty Level"]).reset_index(drop=True)
    df["skills_list"] = df["Skills"].apply(parse_skills)

    log.info("Loaded %d courses after cleaning.", len(df))

    # ------------------------------------------------------------------
    # Flatten skills → parallel lists
    # ------------------------------------------------------------------
    flat_skills: list[str] = []
    flat_course_idx: list[int] = []

    for course_idx, skills in enumerate(df["skills_list"]):
        for skill in skills:
            flat_skills.append(skill)
            flat_course_idx.append(course_idx)

    log.info("Found %d skill tags across all courses.", len(flat_skills))

    # ------------------------------------------------------------------
    # Load model and encode
    # ------------------------------------------------------------------
    log.info("Loading model from %s", MODEL_PATH)
    model = SentenceTransformer(str(MODEL_PATH))

    log.info("Encoding skills (batch_size=256)...")
    embeddings = model.encode(
        flat_skills,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
        batch_size=256,
    )

    # ------------------------------------------------------------------
    # Persist — all paths from config
    # ------------------------------------------------------------------
    np.save(EMBEDDINGS_PATH, embeddings)
    np.save(COURSE_INDEX_PATH, np.array(flat_course_idx, dtype=np.int32))
    np.save(FLAT_SKILLS_PATH, np.array(flat_skills, dtype=object))

    log.info("Embeddings saved to %s", EMBEDDINGS_PATH)
    log.info("Course index saved to %s", COURSE_INDEX_PATH)
    log.info("Flat skills saved to %s", FLAT_SKILLS_PATH)
    log.info("Done.")


if __name__ == "__main__":
    main()