import torch
from sklearn.metrics import roc_auc_score

def evaluate(model, predictor, graph, pos_edges, neg_edges, device='cpu'):
    model.eval()
    predictor.eval()
    with torch.no_grad():
        out = model({k:v.to(device) for k,v in graph.x_dict.items()},
                    {k:v.to(device) for k,v in graph.edge_index_dict.items()})
        js_emb, job_emb = out['JobSeeker'], out['Job']
        pos_scores = predictor(js_emb[pos_edges[0]], job_emb[pos_edges[1]]).cpu()
        neg_scores = predictor(js_emb[neg_edges[0]], job_emb[neg_edges[1]]).cpu()
        y_true = torch.cat([torch.ones(pos_scores.size(0)), torch.zeros(neg_scores.size(0))])
        y_scores = torch.cat([pos_scores, neg_scores])
        return roc_auc_score(y_true.numpy(), y_scores.numpy())

def hit_at_k(model, predictor, graph, pos_edges, k=5, device='cpu'):
    model.eval()
    predictor.eval()
    hits = 0
    total = pos_edges.size(1)
    with torch.no_grad():
        out = model({k:v.to(device) for k,v in graph.x_dict.items()},
                    {k:v.to(device) for k,v in graph.edge_index_dict.items()})
        js_emb, job_emb = out['JobSeeker'], out['Job']
        for i in range(total):
            js = pos_edges[0, i].item()
            true_job = pos_edges[1, i].item()
            js_vec = js_emb[js].unsqueeze(0).repeat(job_emb.size(0),1)
            scores = predictor(js_vec, job_emb)
            top_k_jobs = scores.topk(k).indices.tolist()
            if true_job in top_k_jobs:
                hits += 1
    return hits/total

def precision_at_k(model, predictor, graph, pos_edges, k=5, device='cpu'):
    model.eval()
    predictor.eval()
    precision_scores = []
    with torch.no_grad():
        out = model({k:v.to(device) for k,v in graph.x_dict.items()},
                    {k:v.to(device) for k,v in graph.edge_index_dict.items()})
        js_emb, job_emb = out['JobSeeker'], out['Job']
        for i in range(pos_edges.size(1)):
            js = pos_edges[0, i].item()
            true_job = pos_edges[1, i].item()
            js_vec = js_emb[js].unsqueeze(0).repeat(job_emb.size(0),1)
            scores = predictor(js_vec, job_emb)
            top_k = scores.topk(k).indices.tolist()
            precision_scores.append(1 if true_job in top_k else 0)
    return sum(precision_scores)/len(precision_scores)