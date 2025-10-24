#!/usr/bin/env python3
"""
Modèle GNN pour prédire T2/contraste à partir de structure protéine/molécule
Licence: MIT
Nécessite: pip install torch torch-geometric rdkit scikit-learn
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import Data, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from typing import Tuple, Optional
import os

class QuantumProxyGNN(nn.Module):
    """
    Graph Neural Network pour prédire proxies quantiques (T2, contraste)
    
    Architecture:
    - Input: Graphe moléculaire (atomes=nœuds, liaisons=arêtes)
    - Features: Type atome, charge, hybridation, aromaticité
    - Output: [log(T2_us), contraste_normalized]
    """
    
    def __init__(self, num_node_features: int = 16, hidden_dim: int = 128):
        super().__init__()
        
        self.conv1 = GCNConv(num_node_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, hidden_dim)
        
        # Têtes de prédiction multi-tâche
        self.fc_t2 = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1)
        )
        
        self.fc_contrast = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1)
        )
    
    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        
        # Message passing
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = F.relu(self.conv3(x, edge_index))
        
        # Pooling global
        x = global_mean_pool(x, batch)
        
        # Prédictions
        t2_pred = self.fc_t2(x)
        contrast_pred = torch.sigmoid(self.fc_contrast(x))
        
        return t2_pred, contrast_pred

def mol_to_graph(smiles: str) -> Optional[Data]:
    """
    Convertit SMILES en graphe PyTorch Geometric
    
    Args:
        smiles: String SMILES (ex: 'c1ccccc1' pour benzène)
        
    Returns:
        Data object (graphe avec features atomiques)
    """
    try:
        from rdkit import Chem
        
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        # Features atomiques (16D)
        atom_features = []
        for atom in mol.GetAtoms():
            features = [
                atom.GetAtomicNum(),
                atom.GetTotalDegree(),
                atom.GetFormalCharge(),
                int(atom.GetHybridization()),
                int(atom.GetIsAromatic()),
                atom.GetTotalNumHs(),
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # Padding
            ]
            atom_features.append(features[:16])
        
        x = torch.tensor(atom_features, dtype=torch.float)
        
        # Arêtes (liaisons)
        edge_index = []
        for bond in mol.GetBonds():
            i = bond.GetBeginAtomIdx()
            j = bond.GetEndAtomIdx()
            edge_index.append([i, j])
            edge_index.append([j, i])
        
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        
        return Data(x=x, edge_index=edge_index)
    
    except Exception as e:
        print(f"⚠️ Erreur conversion SMILES: {e}")
        return None

class QuantumProxyTrainer:
    """Pipeline d'entraînement complet"""
    
    def __init__(self, atlas_csv: str = "data/processed/atlas_fp_optical_v1_3.csv"):
        self.atlas_df = pd.read_csv(atlas_csv)
        self.model = QuantumProxyGNN()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
    def prepare_dataset(self) -> Tuple[DataLoader, DataLoader]:
        """
        Prépare dataset PyTorch Geometric depuis atlas
        
        Returns:
            (train_loader, val_loader)
        """
        # Filtrer systèmes avec données complètes
        df = self.atlas_df.dropna(subset=['contrast_normalized'])
        print(f"📊 Dataset: {len(df)} systèmes")
        
        graphs = []
        
        for idx, row in df.iterrows():
            try:
                # PLACEHOLDER: Remplacer par vraie conversion
                smiles = row.get('smiles', 'c1ccccc1')
                graph = mol_to_graph(smiles)
                
                if graph is None:
                    continue
                
                # Labels
                t2 = np.log10(row.get('t2_us', 1.0) + 1e-6)
                contrast = row.get('contrast_normalized', 0.1)
                
                graph.y = torch.tensor([[t2, contrast]], dtype=torch.float)
                graphs.append(graph)
                
            except Exception as e:
                continue
        
        print(f"✅ {len(graphs)} graphes créés")
        
        train_graphs, val_graphs = train_test_split(graphs, test_size=0.2, random_state=42)
        
        train_loader = DataLoader(train_graphs, batch_size=16, shuffle=True)
        val_loader = DataLoader(val_graphs, batch_size=16)
        
        return train_loader, val_loader
    
    def train_epoch(self, loader: DataLoader) -> float:
        """Une époque d'entraînement"""
        self.model.train()
        total_loss = 0
        
        for batch in loader:
            self.optimizer.zero_grad()
            
            t2_pred, contrast_pred = self.model(batch)
            
            t2_target = batch.y[:, 0].unsqueeze(1)
            contrast_target = batch.y[:, 1].unsqueeze(1)
            
            loss_t2 = F.mse_loss(t2_pred, t2_target)
            loss_contrast = F.mse_loss(contrast_pred, contrast_target)
            
            loss = loss_t2 + loss_contrast
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(loader)
    
    def evaluate(self, loader: DataLoader) -> dict:
        """Évaluation validation set"""
        self.model.eval()
        
        all_t2_pred, all_t2_true = [], []
        all_contrast_pred, all_contrast_true = [], []
        
        with torch.no_grad():
            for batch in loader:
                t2_pred, contrast_pred = self.model(batch)
                
                all_t2_pred.extend(t2_pred.numpy().flatten())
                all_t2_true.extend(batch.y[:, 0].numpy())
                
                all_contrast_pred.extend(contrast_pred.numpy().flatten())
                all_contrast_true.extend(batch.y[:, 1].numpy())
        
        return {
            't2_r2': r2_score(all_t2_true, all_t2_pred),
            't2_mae': mean_absolute_error(all_t2_true, all_t2_pred),
            'contrast_r2': r2_score(all_contrast_true, all_contrast_pred),
            'contrast_mae': mean_absolute_error(all_contrast_true, all_contrast_pred)
        }
    
    def run_training(self, epochs: int = 50, save_path: str = "models/quantum_proxy_gnn.pth"):
        """Pipeline complet d'entraînement"""
        train_loader, val_loader = self.prepare_dataset()
        
        best_r2 = -np.inf
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            metrics = self.evaluate(val_loader)
            
            print(f"Epoch {epoch+1}/{epochs}")
            print(f"  Loss: {train_loss:.4f}")
            print(f"  T2 R²: {metrics['t2_r2']:.3f} | MAE: {metrics['t2_mae']:.3f}")
            print(f"  Contrast R²: {metrics['contrast_r2']:.3f} | MAE: {metrics['contrast_mae']:.3f}")
            
            avg_r2 = (metrics['t2_r2'] + metrics['contrast_r2']) / 2
            if avg_r2 > best_r2:
                best_r2 = avg_r2
                torch.save(self.model.state_dict(), save_path)
                print(f"  ✅ Modèle sauvegardé (R²={avg_r2:.3f})")
        
        print(f"\n🎯 Meilleur R² moyen: {best_r2:.3f}")
        return self.model

if __name__ == "__main__":
    print("🧠 Entraînement modèle GNN Quantum Proxies")
    print("⚠️  Nécessite: pip install torch torch-geometric rdkit scikit-learn")
    
    trainer = QuantumProxyTrainer()
    model = trainer.run_training(epochs=50)
    
    print("\n✅ Entraînement terminé!")


