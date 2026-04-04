import torch
from torch_geometric.data import HeteroData
from config import driver, encoder, experience_map

def get_hetero_data(tx):
    data = HeteroData()
    id_maps = {}

    node_configs = {
        "Skill": "name",
        "Job": "title",
        "JobSeeker": "job_title"
    }

    for label, prop in node_configs.items():
        query = f"MATCH (n:{label}) RETURN elementId(n) as id, n.{prop} as text"
        if label != "Skill":
            query = f"MATCH (n:{label}) RETURN elementId(n) as id, n.{prop} as text, n.experience_level as experience"

        result = tx.run(query)

        texts, mapping, experiences = [], {}, []

        for i, rec in enumerate(result):
            mapping[rec['id']] = i
            texts.append(str(rec['text'] if rec['text'] else "unknown"))
            if label != "Skill":
                exp = experience_map.get(rec['experience'], 0)
                experiences.append(exp)

        embeddings = encoder.encode(texts)
        x = torch.tensor(embeddings, dtype=torch.float)

        if label != "Skill":
            exp_tensor = torch.tensor(experiences).float().unsqueeze(1) / 5.0
            x = torch.cat([x, exp_tensor], dim=1)
            data[label].experience = torch.tensor(experiences, dtype=torch.float)

        data[label].x = x
        data[label].text = texts
        id_maps[label] = mapping

        if label == "Job":
            data[label].idx_to_elementId = {i: eid for eid, i in mapping.items()}

    # Add edges
    relations = [("Job", "REQUIRES_SKILL", "Skill"), ("JobSeeker", "HAS_SKILL", "Skill")]
    for src, rel, dst in relations:
        query = f"MATCH (a:{src})-[r:{rel}]->(b:{dst}) RETURN elementId(a) as s, elementId(b) as d"
        result = tx.run(query)
        edges = [[id_maps[src][rec['s']], id_maps[dst][rec['d']]] for rec in result if rec['s'] in id_maps[src] and rec['d'] in id_maps[dst]]
        if edges:
            data[src, rel, dst].edge_index = torch.tensor(edges).t().contiguous()

    return data

def load_hetero_graph():
    with driver.session() as session:
        hetero_graph = session.execute_read(get_hetero_data)

    # Add reverse edges and self-loops
    for (src, rel, dst) in hetero_graph.edge_index_dict.keys():
        rev_key = (dst, rel + "_rev", src)
        if rev_key not in hetero_graph.edge_index_dict:
            hetero_graph[rev_key].edge_index = hetero_graph[src, rel, dst].edge_index.flip(0)

    for node_type in hetero_graph.node_types:
        N = hetero_graph[node_type].num_nodes
        hetero_graph[node_type, 'self_loop', node_type].edge_index = torch.arange(N).unsqueeze(0).repeat(2,1)

    return hetero_graph