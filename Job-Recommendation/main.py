from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import torch
import copy

from recommend import recommend_jobs
from config import encoder
from models import HGTModel, Predictor
from data_loader import load_hetero_graph

# =========================
# DEVICE
# =========================
device = "cpu"

# =========================
# LOAD GRAPH ONCE
# =========================
base_graph = load_hetero_graph()

# =========================
# BUILD MODEL CORRECTLY
# =========================
in_channels_dict = {k: base_graph[k].x.shape[1] for k in base_graph.node_types}

model = HGTModel(
    metadata=base_graph.metadata(),
    in_channels_dict=in_channels_dict,
    hidden=128
).to(device)

# Run one forward pass to infer embedding dim if needed
with torch.no_grad():
    out = model(base_graph.x_dict, base_graph.edge_index_dict)

embed_dim = out["JobSeeker"].shape[1]

predictor = Predictor(dim=embed_dim).to(device)

# =========================
# LOAD TRAINED WEIGHTS
# =========================
model.load_state_dict(torch.load("saved/model.pt", map_location=device))
predictor.load_state_dict(torch.load("saved/predictor.pt", map_location=device))

model.eval()
predictor.eval()

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Job Recommendation API",
    version="1.0.0"
)

# =========================
# REQUEST SCHEMA
# =========================
class RecommendRequest(BaseModel):
    user_skills: List[str]
    user_experience: str
    top_k: int = 5

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"message": "Job Recommendation API is running"}

# =========================
# RECOMMEND ENDPOINT
# =========================
@app.post("/recommend")
def recommend(request: RecommendRequest):
    try:
        # IMPORTANT: clone/copy graph per request
        graph = copy.deepcopy(base_graph)

        recommendations = recommend_jobs(
            user_skills=request.user_skills,
            user_experience=request.user_experience,
            model=model,
            predictor=predictor,
            graph=graph,
            encoder=encoder,
            top_k=request.top_k,
            device=device
        )

        return {
            "success": True,
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )