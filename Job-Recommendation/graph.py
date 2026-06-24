"""
Builds the HeteroData graph from Neo4j — mirrors the notebook's get_hetero_data().
"""

import torch
from neo4j import GraphDatabase
from torch_geometric.data import HeteroData
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


def _get_hetero_data(tx, encoder: SentenceTransformer):
    data = HeteroData()
    id_maps = {}

    node_configs = {
        "Skill": "name",
        "Job": "title",
        "JobSeeker": "job_title",
    }

    for label, prop in node_configs.items():
        if label == "Skill":
            query = f"MATCH (n:{label}) RETURN elementId(n) as id, n.{prop} as text"
        else:
            query = (
                f"MATCH (n:{label}) "
                f"RETURN elementId(n) as id, n.{prop} as text, n.experience_level as experience"
            )

        result = tx.run(query)
        texts, mapping, experiences = [], {}, []

        for i, rec in enumerate(result):
            mapping[rec["id"]] = i
            text = rec["text"] if rec["text"] else "unknown"
            texts.append(str(text))

            if label != "Skill":
                exp = experience_map.get(rec["experience"], 0)
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

    relations = [
        ("Job", "REQUIRES_SKILL", "Skill"),
        ("JobSeeker", "HAS_SKILL", "Skill"),
    ]

    for src, rel, dst in relations:
        query = (
            f"MATCH (a:{src})-[r:{rel}]->(b:{dst}) "
            f"RETURN elementId(a) as s, elementId(b) as d"
        )
        result = tx.run(query)

        edges = []
        for rec in result:
            if rec["s"] in id_maps[src] and rec["d"] in id_maps[dst]:
                edges.append([id_maps[src][rec["s"]], id_maps[dst][rec["d"]]])

        if edges:
            data[src, rel, dst].edge_index = torch.tensor(edges).t().contiguous()

    return data


def build_graph(uri: str, user: str, password: str):
    """
    Connect to Neo4j, build the heterogeneous graph, add reverse edges & self-loops.

    Returns:
        (hetero_graph, in_channels_dict, encoder)
    """
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        hetero_graph = session.execute_read(_get_hetero_data, encoder)

    driver.close()

    # Add reverse edges
    for src, rel, dst in list(hetero_graph.edge_index_dict.keys()):
        rev_key = (dst, rel + "_rev", src)
        if rev_key not in hetero_graph.edge_index_dict:
            hetero_graph[rev_key].edge_index = hetero_graph[src, rel, dst].edge_index.flip(0)

    # Add self-loops
    for node_type in hetero_graph.node_types:
        N = hetero_graph[node_type].num_nodes
        hetero_graph[node_type, "self_loop", node_type].edge_index = (
            torch.arange(N).unsqueeze(0).repeat(2, 1)
        )

    in_channels_dict = {k: hetero_graph[k].x.shape[1] for k in hetero_graph.node_types}

    return hetero_graph, in_channels_dict, encoder