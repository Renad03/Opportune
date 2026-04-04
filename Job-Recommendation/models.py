import torch
import torch.nn.functional as F
from torch_geometric.nn import HGTConv

class HGTModel(torch.nn.Module):
    def __init__(self, metadata, in_channels_dict, hidden=128, dropout=0.2):
        super().__init__()
        self.dropout = dropout
        self.convs = torch.nn.ModuleList([
            HGTConv(in_channels_dict, hidden, metadata, heads=2),
            HGTConv(hidden, hidden, metadata, heads=2)
        ])
    def forward(self, x_dict, edge_index_dict):
        for conv in self.convs:
            x_dict = conv(x_dict, edge_index_dict)
            x_dict = {k: F.dropout(F.relu(v), p=self.dropout, training=self.training) for k,v in x_dict.items()}
        return x_dict

class Predictor(torch.nn.Module):
    def __init__(self, dim, dropout=0.2):
        super().__init__()
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(dim*2, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(dropout),
            torch.nn.Linear(128,1)
        )
    def forward(self, x1, x2):
        return self.mlp(torch.cat([x1,x2], dim=1)).squeeze()