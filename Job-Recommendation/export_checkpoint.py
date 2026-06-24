"""
Run this in your Colab/Jupyter notebook AFTER training to export a checkpoint
that the API can load without needing to re-run the graph forward pass.

Usage (in Colab):
    exec(open("export_checkpoint.py").read())
    # or just paste the code into a cell
"""

import torch

# ── assumes `model`, `predictor`, `out`, `best_val_score` are already in scope ──

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

print(f"✅ Saved final_model.pt  (embed_dim={embed_dim})")