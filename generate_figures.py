#!/usr/bin/env python3
"""
Génère les figures statiques pour le README de l'Atlas des Qubits Biologiques.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration du style
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Création du dossier figures s'il n'existe pas
if not os.path.exists('figures'):
    os.makedirs('figures')
    print("Dossier 'figures/' créé.")

# Chargement des données
try:
    df = pd.read_csv('biological_qubits.csv')
    print(f"Dataset 'biological_qubits.csv' chargé ({len(df)} lignes).")
except FileNotFoundError:
    print("Erreur: Le fichier 'biological_qubits.csv' est introuvable.")
    exit()

# Nettoyage des données pour les graphiques
df['Temperature_K'] = pd.to_numeric(df['Temperature_K'], errors='coerce')
df['T2_us'] = pd.to_numeric(df['T2_us'], errors='coerce')
df['Annee'] = pd.to_numeric(df['Annee'], errors='coerce')
df.dropna(subset=['Temperature_K', 'T2_us', 'Classe', 'Methode_lecture', 'Annee'], inplace=True)
print(f"Données nettoyées, {len(df)} lignes valides pour les graphiques.")


# --- Figure 1: T2 vs Température ---
print("Génération de fig_t2_vs_temp.png...")
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=df,
    x='Temperature_K',
    y='T2_us',
    hue='Classe',
    style='Methode_lecture',
    size='Qualite',
    sizes=(50, 250),
    alpha=0.8,
    edgecolor='w',
    linewidth=1
)

plt.yscale('log')
plt.xscale('log')

plt.title('Temps de cohérence (T2) vs Température', fontsize=18, pad=20)
plt.xlabel('Température (K) [échelle log]', fontsize=14)
plt.ylabel('T2 (µs) [échelle log]', fontsize=14)

plt.grid(True, which="both", ls="--", c='0.7')
handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Légende')
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Annotations pour les points clés
df_annot = df[df['T2_us'] > 10] # Annoter les points les plus performants
for i, row in df_annot.iterrows():
    plt.text(row['Temperature_K'] * 1.1, row['T2_us'], row['Systeme'], fontsize=8, alpha=0.8)

plt.savefig('figures/fig_t2_vs_temp.png', dpi=300, bbox_inches='tight')
print(" -> Figure sauvegardée.")

# --- Figure 2: Timeline des publications ---
print("Génération de fig_pub_timeline.png...")
plt.figure(figsize=(12, 7))
yearly_counts = df['Annee'].value_counts().sort_index()

barplot = sns.barplot(
    x=yearly_counts.index.astype(int),
    y=yearly_counts.values,
    palette='magma'
)

plt.title('Timeline des publications de systèmes référencés', fontsize=18, pad=20)
plt.xlabel('Année de publication', fontsize=14)
plt.ylabel('Nombre de systèmes publiés', fontsize=14)
plt.xticks(rotation=45)

# Ajouter le nombre au-dessus de chaque barre
for i in barplot.patches:
    barplot.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, \
                f'{int(i.get_height())}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('figures/fig_pub_timeline.png', dpi=300)
print(" -> Figure sauvegardée.")

print("\nScript terminé avec succès.")
