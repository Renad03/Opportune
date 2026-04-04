import torch
import random
from sklearn.model_selection import train_test_split

def generate_positive_pairs(data, encoder, threshold=0.4, device='cpu'):
    skill_texts = data['Skill'].text
    skill_embeddings = encoder.encode(skill_texts, convert_to_tensor=True, device=device, normalize_embeddings=True)

    js_skills_idx = {}
    for js, sk in data['JobSeeker','HAS_SKILL','Skill'].edge_index.t().tolist():
        js_skills_idx.setdefault(js, []).append(sk)

    job_skills_idx = {}
    for job, sk in data['Job','REQUIRES_SKILL','Skill'].edge_index.t().tolist():
        job_skills_idx.setdefault(job, []).append(sk)

    js_embs = {js: skill_embeddings[idx_list].mean(dim=0) for js, idx_list in js_skills_idx.items()}
    job_embs = {job: skill_embeddings[idx_list].mean(dim=0) for job, idx_list in job_skills_idx.items()}

    pos = [[js, job] for js, js_emb in js_embs.items() for job, job_emb in job_embs.items() if (js_emb @ job_emb).item() >= threshold]
    return torch.tensor(pos, dtype=torch.long).t() if pos else torch.empty((2,0), dtype=torch.long)

def hard_negative_sampling(data, pos_edge_index, num_samples):
    pos_set = set(map(tuple, pos_edge_index.t().tolist()))
    neg = set()
    js_nodes = list(range(data['JobSeeker'].num_nodes))
    job_nodes = list(range(data['Job'].num_nodes))
    while len(neg) < num_samples:
        js = random.choice(js_nodes)
        job = random.choice(job_nodes)
        if (js, job) not in pos_set:
            neg.add((js, job))
    return torch.tensor(list(neg)).t()

def split_edges(edge_index, test_size=0.2, val_size=0.5):
    edges = edge_index.t().numpy()
    train, temp = train_test_split(edges, test_size=test_size, random_state=42)
    val, test = train_test_split(temp, test_size=val_size, random_state=42)
    return torch.tensor(train).t(), torch.tensor(val).t(), torch.tensor(test).t()