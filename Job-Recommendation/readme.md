# Job Recommender API

FastAPI wrapper for the HGT-based job recommendation model.

---

## Project Structure

```
job_recommender_api/
├── main.py               # FastAPI app & routes
├── model.py              # HGTModel + Predictor classes
├── graph.py              # Neo4j → HeteroData builder
├── recommend.py          # Core recommendation logic
├── config.py             # Settings (env vars / .env)
├── export_checkpoint.py  # Run in Colab to export the model
├── requirements.txt
└── .env.example
```

---

## Step 1 — Export Your Checkpoint (Colab)

In your notebook, after training run:

```python
import torch

with torch.no_grad():
    _out = model(hetero_graph.x_dict, hetero_graph.edge_index_dict)

embed_dim = _out["JobSeeker"].shape[1]

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "predictor_state_dict": predictor.state_dict(),
        "embed_dim": embed_dim,
        "best_val_score": best_val_score,
    },
    "final_model.pt",
)
```

Then download `final_model.pt` and place it next to `main.py`.

---

## Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: `torch-geometric` may need extra index URLs depending on your CUDA version.
> See https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html

---

## Step 3 — Configure Environment

```bash
cp .env.example .env
# Edit .env — set CHECKPOINT_PATH, HIDDEN_DIM, NUM_LAYERS, DROPOUT
# to match what you used during training (especially if Optuna changed them).
```

---

## Step 4 — Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Interactive docs: http://localhost:8000/docs

---

## Endpoints

| Method | Path               | Description                        |
|--------|--------------------|------------------------------------|
| GET    | /health            | Liveness check                     |
| GET    | /skills            | List all skills in the graph       |
| GET    | /experience-levels | List valid experience level values |
| POST   | /recommend         | Get job recommendations            |

---

## Example Request

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Docker", "FastAPI", "AWS", "Pandas"],
    "experience": "senior",
    "top_k": 5
  }'
```

### Example Response

```json
{
  "recommendations": [
    {
      "job_title": "Data Engineer",
      "recommended_skills": ["Python", "AWS", "Airflow", "Pandas", "Docker"],
      "contributing_skills": ["python", "aws", "pandas", "docker"],
      "final_score": 1.3842
    }
  ],
  "matched_skills": ["Python", "Docker", "AWS", "Pandas"],
  "unmatched_skills": ["FastAPI"]
}
```

---

## Architecture Notes

- On startup the API connects to Neo4j, rebuilds the graph, and loads model weights — this takes ~30s.
- The graph is held in memory; no database call is made per request.
- The `embed_dim` is read from the checkpoint, so it always matches the predictor's input size.
- Thread safety: `recommend_jobs()` temporarily mutates the graph but always restores it.
  For high-concurrency production use, add a lock or clone the graph per request.