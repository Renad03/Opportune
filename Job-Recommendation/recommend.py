import torch
def recommend_jobs(user_skills, user_experience, model, predictor, graph, encoder, top_k=5, device='cpu'):
    """
    Recommend jobs for a new user based on skills and experience using HGT + predictor.

    Args:
        user_skills (list[str]): List of user's skills (lowercase recommended).
        user_experience (str): Experience level ("intern", "junior", "mid", "senior", "lead").
        model (HGTModel): Trained HGT model.
        predictor (Predictor): Trained predictor.
        graph (HeteroData): Heterogeneous graph containing Job, Skill, JobSeeker nodes.
        encoder (SentenceTransformer): Encoder to embed skill/job texts.
        top_k (int): Number of top job recommendations to return.
        device (str): 'cpu' or 'cuda'.

    Returns:
        list[dict]: List of recommended jobs with contributing skills.
    """
    
    experience_map = {
    "intern": 0,
    "fresher": 1,
    "junior": 2,
    "mid": 3,
    "senior": 4,
    "lead": 5,
    "unspecified": 0
    }
    
    model.eval()
    predictor.eval()

    # 1️⃣ Prepare user skill embeddings
    user_skills_lower = [s.lower() for s in user_skills]
    skill_texts = [s.lower() for s in graph['Skill'].text]
    skill_indices = [i for i, s in enumerate(skill_texts) if s in user_skills_lower]

    if not skill_indices:
        print("Warning: None of the user skills match existing skills in the graph.")
        return []

    # Encode user as a vector with experience appended
    exp_value = experience_map.get(user_experience.lower(), 0) / 5.0
    skill_embs = graph['Skill'].x[skill_indices]  # shape: [num_user_skills, skill_dim]
    user_emb = skill_embs.mean(dim=0, keepdim=True)
    user_emb = torch.cat([user_emb, torch.tensor([[exp_value]], dtype=torch.float)], dim=1).to(device)

    # 2️⃣ Temporarily add a new JobSeeker node
    original_js_x = graph['JobSeeker'].x.clone()
    new_js_idx = graph['JobSeeker'].num_nodes
    graph['JobSeeker'].x = torch.cat([graph['JobSeeker'].x, user_emb], dim=0)

    # 3️⃣ Temporarily add HAS_SKILL edges for the new user
    if ('JobSeeker', 'HAS_SKILL', 'Skill') in graph.edge_index_dict:
        orig_edges = graph['JobSeeker', 'HAS_SKILL', 'Skill'].edge_index
    else:
        orig_edges = torch.empty((2,0), dtype=torch.long)

    new_edges = torch.tensor([[new_js_idx]*len(skill_indices), skill_indices], dtype=torch.long)
    graph['JobSeeker', 'HAS_SKILL', 'Skill'].edge_index = torch.cat([orig_edges, new_edges], dim=1)

    # 4️⃣ Forward pass through HGT
    with torch.no_grad():
        out = model({k: v.to(device) for k,v in graph.x_dict.items()},
                    {k: v.to(device) for k,v in graph.edge_index_dict.items()})

    js_emb = out['JobSeeker']
    job_emb = out['Job']

    # 5️⃣ Score all jobs
    user_vec = js_emb[new_js_idx].unsqueeze(0).repeat(job_emb.size(0), 1)
    scores = predictor(user_vec, job_emb).cpu()

    # 6️⃣ Rank jobs and filter by contributing skills
    ranked_indices = scores.topk(top_k*25).indices.tolist()  # get more to filter later
    recommended_jobs = []

    for idx in ranked_indices:
        job_title = graph['Job'].text[idx]
        job_skills = [graph['Skill'].text[s] for s in graph['Job','REQUIRES_SKILL','Skill'].edge_index[1][
            (graph['Job','REQUIRES_SKILL','Skill'].edge_index[0]==idx)
        ].tolist()]

        contributing_skills = [s for s in job_skills if s.lower() in user_skills_lower]
        if not contributing_skills:
            continue  # skip jobs with no actual matching skills

        recommended_jobs.append({
            'job_title': job_title,
            'recommended_skills': job_skills,
            'contributing_skills': contributing_skills
        })

        if len(recommended_jobs) >= top_k:
            break

    # 7️⃣ Restore original graph
    graph['JobSeeker'].x = original_js_x
    graph['JobSeeker','HAS_SKILL','Skill'].edge_index = orig_edges

    return recommended_jobs