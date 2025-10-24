# 📊 Dashboard Interactif — Guide Utilisateur

**Version** : 2.0  
**Date** : 24 octobre 2025  
**Dashboard** : `index_v2_interactive.html`

---

## 🎯 Vue d'Ensemble

Le **Dashboard Interactif Biological Qubits Atlas** offre une exploration visuelle des 200+ systèmes quantiques biologiques avec :

- 📊 **Scatter plot** T2 vs Température (interactif)
- 📊 **Barplot** familles (trié par nombre de systèmes)
- 📊 **Statistiques temps réel** (filtrage dynamique)
- 📊 **Timeline** publications (évolution temporelle)

**Technologies** : D3.js v7, HTML5, CSS3 (pur JavaScript, pas de framework)

---

## 🚀 Quick Start (2 minutes)

### Étape 1 : Générer Dashboard

```bash
cd /path/to/Quantum-Sensors-Qubits-in-Biology
python scripts/web/generate_interactive_dashboard.py
```

**Output** : `index_v2_interactive.html`

### Étape 2 : Lancer Serveur Local

```bash
# Option A : Python
python -m http.server 8000

# Option B : Node.js
npx http-server -p 8000
```

### Étape 3 : Ouvrir Dashboard

Navigateur → `http://localhost:8000/index_v2_interactive.html`

---

## 📊 Visualisations Disponibles

### 1. Scatter Plot T2 vs Température

**Localisation** : Section supérieure du dashboard

**Fonctionnalités** :
- **Axes** :
  - X : Température (K) — 270 à 320 K
  - Y : Contraste normalisé (fold-change) — log scale
  
- **Points** :
  - Couleur : Famille (Calcium, Voltage, Dopamine, etc.)
  - Taille : Fixe (6px), agrandit au survol (10px)
  - Opacité : 0.7 (semi-transparent pour voir chevauchements)

- **Interactions** :
  - **Survol** : Tooltip affiche nom, famille, contraste, température, DOI
  - **Clic légende** : Masquer/afficher famille
  - **Zoom** : Scroll molette (si activé dans future version)

**Exemple Tooltip** :
```
GCaMP6f
Family: Calcium
Contrast: 16.5-fold
Temp: 298 K
DOI: 10.1038/nature12354
```

---

### 2. Barplot Familles

**Localisation** : Section milieu du dashboard

**Fonctionnalités** :
- **Axes** :
  - X : Familles (Calcium, Voltage, Dopamine, etc.)
  - Y : Nombre de systèmes

- **Barres** :
  - Couleur : Selon famille (même code couleur que scatter)
  - Hauteur : Proportionnelle au nombre de systèmes
  - Largeur : Automatique (padding 0.2)

- **Interactions** :
  - **Survol** : Tooltip affiche nombre exact
  - **Clic** : Filtre scatter plot (future version)

**Tri** : Décroissant par nombre de systèmes

---

### 3. Statistiques Temps Réel

**Localisation** : Haut de page (cartes)

**Métriques Affichées** :
- **Total Systems** : 200+ (ou nombre actuel)
- **With T2 Data** : Nombre avec T2 mesuré
- **Families** : Nombre familles uniques
- **In Vivo** : Systèmes validés in vivo

**Mise à Jour** : Automatique lors filtrage (future)

---

## 🎨 Personnalisation

### Modifier Couleurs

Éditer `index_v2_interactive.html`, section `<style>` :

```css
/* Exemple : Changer gradient background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Remplacer par vos couleurs */
}

/* Exemple : Changer couleur stat-cards */
.stat-value {
    color: #667eea; /* Violet par défaut */
}
```

### Modifier Tailles Graphiques

Éditer `<script>` section, variables `width` et `height` :

```javascript
const width = 1200;  // Largeur scatter plot (pixels)
const height = 600;  // Hauteur scatter plot (pixels)
```

---

## 🔍 Filtrage & Recherche (Future)

**Fonctionnalités Prévues v2.1** :
- [ ] Recherche textuelle (nom protéine)
- [ ] Filtres dropdown (Famille, Contexte, Qualité)
- [ ] Slider température (plage sélectionnable)
- [ ] Export données filtrées (CSV)

**Workaround Actuel** : Clic légende pour masquer familles

---

## 📥 Export Graphiques

### Export SVG (Haute Résolution)

**Méthode Manuelle** :
1. Ouvrir dashboard dans navigateur
2. Clic droit sur graphique → "Inspecter"
3. Localiser balise `<svg>`
4. Copier contenu SVG
5. Sauvegarder dans fichier `.svg`

**Résolution** : Vectoriel (scalable infini)

### Export PNG (Publications)

**Méthode Navigateur** :
1. Ouvrir dashboard
2. F12 → Console → Coller :
```javascript
// Sélectionner SVG
const svg = document.querySelector('#scatter-t2-temp svg');

// Convertir en canvas
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 1200;
canvas.height = 600;

const img = new Image();
img.src = 'data:image/svg+xml;base64,' + btoa(svg.outerHTML);
img.onload = () => {
    ctx.drawImage(img, 0, 0);
    const link = document.createElement('a');
    link.download = 'scatter_plot.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
};
```

**Résolution** : 300 dpi (configurablevia `canvas.width/height`)

---

## 🐛 Troubleshooting

### Problème : Dashboard Vide / Pas de Données

**Cause** : Politique CORS (Cross-Origin Resource Sharing)

**Solution** : Lancer serveur local (voir Quick Start)

**NE PAS** : Ouvrir fichier HTML directement (`file://`)

---

### Problème : Graphiques Ne S'Affichent Pas

**Diagnostic** :
1. F12 → Console → Vérifier erreurs JavaScript
2. Vérifier message : "Failed to load resource: net::ERR_FILE_NOT_FOUND"

**Solutions** :
- **Si erreur D3.js CDN** : Vérifier connexion internet
- **Si erreur CSV** : Vérifier chemin fichier dans HTML (ligne ~210)
- **Si erreur syntax** : Regénérer dashboard avec script Python

---

### Problème : Dashboard Lent (>5s chargement)

**Causes Possibles** :
- Dataset trop volumineux (>1000 systèmes)
- Navigateur ancien (IE11, Safari <12)

**Solutions** :
- Utiliser navigateur moderne (Chrome 90+, Firefox 88+)
- Réduire dataset (filtrer avant génération)
- Activer GPU acceleration (Chrome flags)

---

### Problème : Tooltip Ne S'Affiche Pas

**Cause** : z-index CSS conflictuel

**Solution** : Éditer `<style>` section :
```css
.tooltip {
    z-index: 9999; /* Augmenter si besoin */
}
```

---

## 📱 Compatibilité Mobile

**Testé Sur** :
- ✅ Chrome Android 90+
- ✅ Safari iOS 14+
- ✅ Firefox Mobile 88+

**Limitations** :
- ⚠️ Tooltip moins précis (touch vs mouse)
- ⚠️ Zoom désactivé par défaut (viewport fixed)

**Optimisations Future** :
- [ ] Touch gestures (pinch-to-zoom)
- [ ] Orientation portrait adaptée
- [ ] Menu hamburger pour filtres

---

## 🔒 Sécurité & Vie Privée

**Données Locales** : Dashboard charge CSV local, **aucune donnée envoyée** vers serveurs externes

**CDN Utilisés** :
- D3.js (d3js.org) — bibliothèque visualisation
- **Aucun tracker** (Google Analytics, etc.)

**Conformité RGPD** : ✅ (pas de cookies, pas de tracking)

---

## 🚀 Améliorations Futures (Roadmap)

### v2.1 (1-2 mois)
- [ ] Filtres interactifs (dropdown, sliders)
- [ ] Recherche textuelle
- [ ] Export SVG/PNG intégré (bouton)
- [ ] Mode sombre

### v2.2 (3-4 mois)
- [ ] Network graph (relations famille-méthode)
- [ ] Timeline publications (évolution temporelle)
- [ ] Heatmap corrélations (T2 vs Contraste vs Temp)

### v3.0 (6+ mois)
- [ ] Backend API (filtres côté serveur)
- [ ] Authentification utilisateur (upload données)
- [ ] Comparaison ML prédictions vs mesures

---

## 📚 Ressources

**Documentation D3.js** : https://d3js.org/  
**Exemples Gallery** : https://observablehq.com/@d3/gallery  
**Tutoriel Interactif** : https://www.d3-graph-gallery.com/

**Code Source Dashboard** : `scripts/web/generate_interactive_dashboard.py`

---

## 📧 Support

**Issues GitHub** : https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues

**Label** : `[dashboard]` pour questions spécifiques dashboard

---

**⚛️ Bon exploration du Dashboard ! 🧬**

📅 Dernière MAJ : 2025-10-24  
✍️ Auteur : Tommy Lepesteur  
🔗 Version : 2.0


