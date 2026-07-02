"""
Recommendation logic.
All state (model, embeddings, dataframe) is passed in explicitly —
no globals, no import-time I/O.
"""

import logging
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

from config import MIN_SIMILARITY

log = logging.getLogger(__name__)

DIFFICULTY_MAP = {
    "beginner":     "Beginner",
    "intermediate": "Intermediate",
    "advanced":     "Advanced",
}


@dataclass
class CourseMatch:
    missing_skill:  str
    course_name:    str
    matched_skill:  str
    match_score:    float
    difficulty:     str
    rating:         float | None
    url:            str | None


def _find_top_courses(
    model:            SentenceTransformer,
    skill:            str,
    skill_embeddings: np.ndarray,
    flat_skills:      np.ndarray,
    flat_course_idx:  np.ndarray,
    df:               pd.DataFrame,
    target_level:     str,
    already_seen:     set[str],
    n:                int,
) -> list[CourseMatch]:
    """
    Returns up to `n` best-matching courses for a single skill.
    Pass 1: fill slots from target difficulty.
    Pass 2: fill remaining slots from any difficulty.
    Skips courses already in `already_seen`.
    """
    query_vec = model.encode(
        [skill],
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    embeddings_tensor = torch.from_numpy(skill_embeddings)
    scores = util.cos_sim(query_vec, embeddings_tensor)[0]
    ranked = scores.argsort(descending=True).tolist()

    def _build_match(idx: int) -> CourseMatch:
        row = df.iloc[int(flat_course_idx[idx])]
        return CourseMatch(
            missing_skill=skill,
            course_name=str(row["Course Name"]),
            matched_skill=str(flat_skills[idx]),
            match_score=round(float(scores[idx]), 3),
            difficulty=str(row["Difficulty Level"]),
            rating=row.get("Course Rating"),
            url=row.get("Course URL"),
        )

    results: list[CourseMatch] = []
    # track course names added in this call so we don't duplicate within the skill
    local_seen: set[str] = set(already_seen)
    visited_row_idxs: set[int] = set()

    # Pass 1 — preferred difficulty
    for idx in ranked:
        if len(results) >= n:
            return results
        if float(scores[idx]) < MIN_SIMILARITY:
            break
        course_idx = int(flat_course_idx[idx])
        if course_idx in visited_row_idxs:
            continue
        visited_row_idxs.add(course_idx)
        row = df.iloc[course_idx]
        course_name = str(row["Course Name"])
        if course_name in local_seen:
            continue
        if row["Difficulty Level"] == target_level:
            results.append(_build_match(idx))
            local_seen.add(course_name)

    if len(results) >= n:
        return results

    # Pass 2 — any difficulty to fill remaining slots
    visited_row_idxs.clear()
    for idx in ranked:
        if len(results) >= n:
            break
        if float(scores[idx]) < MIN_SIMILARITY:
            break
        course_idx = int(flat_course_idx[idx])
        if course_idx in visited_row_idxs:
            continue
        visited_row_idxs.add(course_idx)
        course_name = str(df.iloc[course_idx]["Course Name"])
        if course_name not in local_seen:
            results.append(_build_match(idx))
            local_seen.add(course_name)

    if not results:
        log.debug("No match above MIN_SIMILARITY (%.2f) for skill '%s'.", MIN_SIMILARITY, skill)
    return results


def recommend_courses(
    model:            SentenceTransformer,
    df:               pd.DataFrame,
    skill_embeddings: np.ndarray,
    flat_skills:      np.ndarray,
    flat_course_idx:  np.ndarray,
    missing_skills:   list[str],
    experience_level: str,
    top_k:            int,
    courses_per_skill: int = 5,
) -> list[dict]:
    """
    Returns up to `courses_per_skill` courses per missing skill, capped at `top_k` total.
    """
    target_level = DIFFICULTY_MAP.get(experience_level.lower(), "Intermediate")
    recommendations: list[dict] = []
    seen_courses: set[str] = set()

    for i, skill in enumerate(missing_skills):
        remaining_skills = len(missing_skills) - i
        remaining_slots  = top_k - len(recommendations)
        n = min(courses_per_skill, math.ceil(remaining_slots / remaining_skills))

        matches = _find_top_courses(
            model=model,
            skill=skill,
            skill_embeddings=skill_embeddings,
            flat_skills=flat_skills,
            flat_course_idx=flat_course_idx,
            df=df,
            target_level=target_level,
            already_seen=seen_courses,
            n=n,
        )

        for match in matches:
            seen_courses.add(match.course_name)
            recommendations.append({
                "missing_skill":  match.missing_skill,
                "course_name":    match.course_name,
                "matched_skill":  match.matched_skill,
                "match_score":    match.match_score,
                "difficulty":     match.difficulty,
                "rating":         match.rating,
                "url":            match.url,
            })

    log.info(
        "Returning %d recommendations for %d missing skills.",
        len(recommendations), len(missing_skills),
    )
    return recommendations
