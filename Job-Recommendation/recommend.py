"""
Core recommendation function — mirrors the notebook's recommend_jobs().
"""

from typing import List, Dict, Any
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

experience_map = {
    "intern": 0,
    "fresher": 1,
    "junior": 2,
    "mid": 3,
    "senior": 4,
    "lead": 5,
    "unspecified": -1,
}


def recommend_jobs(
    user_skills: List[str],
    user_experience: str,
    model,
    predictor,
    graph,
    encoder: SentenceTransformer,
    top_k: int = 5,
    device: str = "cpu",
) -> List[Dict[str, Any]]:
    """
    Recommend jobs for a user given their skills and experience.

    Returns a list of dicts with keys:
        job_title, recommended_skills, contributing_skills, final_score
    """
    model.eval()
    predictor.eval()

    user_skills_lower = [s.lower() for s in user_skills]
    skill_texts = [s.lower() for s in graph["Skill"].text]
    skill_indices = [i for i, s in enumerate(skill_texts) if s in user_skills_lower]

    if not skill_indices:
        return []

    # Build user embedding
    exp_value = experience_map.get(user_experience.lower(), 0) / 5.0
    skill_embs = graph["Skill"].x[skill_indices]
    user_emb = skill_embs.mean(dim=0, keepdim=True)
    user_emb = torch.cat(
        [user_emb, torch.tensor([[exp_value]], dtype=torch.float)], dim=1
    ).to(device)

    # Temporarily insert a new JobSeeker node
    original_js_x = graph["JobSeeker"].x.clone()
    new_js_idx = graph["JobSeeker"].num_nodes
    graph["JobSeeker"].x = torch.cat([graph["JobSeeker"].x, user_emb], dim=0)

    orig_edges = graph.get(
        ("JobSeeker", "HAS_SKILL", "Skill"), {}
    ).get("edge_index", torch.empty((2, 0), dtype=torch.long))

    new_edges = torch.tensor(
        [[new_js_idx] * len(skill_indices), skill_indices], dtype=torch.long
    )
    graph["JobSeeker", "HAS_SKILL", "Skill"].edge_index = torch.cat(
        [orig_edges, new_edges], dim=1
    )

    # Forward pass
    with torch.no_grad():
        out = model(
            {k: v.to(device) for k, v in graph.x_dict.items()},
            {k: v.to(device) for k, v in graph.edge_index_dict.items()},
        )

    js_emb = out["JobSeeker"]
    job_emb = out["Job"]

    user_vec = js_emb[new_js_idx].unsqueeze(0).repeat(job_emb.size(0), 1)
    scores = predictor(user_vec, job_emb).cpu()

    # Score & rank
    job_edge_index = graph["Job", "REQUIRES_SKILL", "Skill"].edge_index
    ranked = []

    for idx in range(job_emb.size(0)):
        job_skill_indices = job_edge_index[1][job_edge_index[0] == idx].tolist()
        job_skills = [graph["Skill"].text[s] for s in job_skill_indices]

        match_skills = [s.lower() for s in job_skills if s.lower() in user_skills_lower]
        if not match_skills:
            continue

        contribution_score = len(match_skills) / max(len(job_skills), 1)
        final_score = scores[idx].item() + 0.5 * contribution_score

        ranked.append((idx, final_score, match_skills, job_skills))

    ranked.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, final_score, contributing, job_skills in ranked[:top_k]:
        results.append(
            {
                "job_title": graph["Job"].text[idx],
                "recommended_skills": job_skills,
                "contributing_skills": contributing,
                "final_score": round(final_score, 4),
            }
        )

    # Restore graph
    graph["JobSeeker"].x = original_js_x
    graph["JobSeeker", "HAS_SKILL", "Skill"].edge_index = orig_edges

    return results