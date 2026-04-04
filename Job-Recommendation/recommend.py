import torch
from config import experience_map

def recommend_jobs(user_skills, user_experience, model, predictor, graph, encoder, top_k=5, device='cpu'):
    model.eval()
    predictor.eval()

    user_skills_lower = [s.lower() for s in user_skills]
    skill_texts = [s.lower() for s in graph['Skill'].text]
    skill_indices = [i for i, s in enumerate(skill_texts) if s in user_skills_lower]
    if not skill_indices:
        print("Warning: No user skills found in graph.")
        return []

    exp_value = experience_map.get(user_experience.lower(), 0)/5.0
    skill_embs = graph['Skill'].x[skill_indices]
    user_emb = torch.cat([skill_embs.mean(dim=0, keepdim=True), torch.tensor([[exp_value]], dtype=torch.float)], dim=1).to(device)

    original_js_x = graph['JobSeeker'].x.clone()
    new_js_idx = graph['JobSeeker'].num_nodes
    graph['JobSeeker'].x = torch.cat([graph['JobSeeker'].x, user_emb], dim=0)

    orig_edges = graph['JobSeeker','HAS_SKILL','Skill'].edge_index if ('JobSeeker','HAS_SKILL','Skill') in graph.edge_index_dict else torch.empty((2,0), dtype=torch.long)
    new_edges = torch.tensor([[new_js_idx]*len(skill_indices), skill_indices], dtype=torch.long)
    graph['JobSeeker','HAS_SKILL','Skill'].edge_index = torch.cat([orig_edges, new_edges], dim=1)

    with torch.no_grad():
        out = model({k:v.to(device) for k,v in graph.x_dict.items()},
                    {k:v.to(device) for k,v in graph.edge_index_dict.items()})

    js_emb, job_emb = out['JobSeeker'], out['Job']
    user_vec = js_emb[new_js_idx].unsqueeze(0).repeat(job_emb.size(0),1)
    scores = predictor(user_vec, job_emb).cpu()
    ranked_indices = scores.topk(top_k*3).indices.tolist()

    recommended_jobs = []
    for idx in ranked_indices:
        job_title = graph['Job'].text[idx]
        job_skills = [graph['Skill'].text[s] for s in graph['Job','REQUIRES_SKILL','Skill'].edge_index[1][(graph['Job','REQUIRES_SKILL','Skill'].edge_index[0]==idx)].tolist()]
        contributing_skills = [s for s in job_skills if s.lower() in user_skills_lower]
        if not contributing_skills:
            continue
        recommended_jobs.append({'job_title': job_title, 'recommended_skills': job_skills, 'contributing_skills': contributing_skills})
        if len(recommended_jobs) >= top_k:
            break

    graph['JobSeeker'].x = original_js_x
    graph['JobSeeker','HAS_SKILL','Skill'].edge_index = orig_edges

    return recommended_jobs