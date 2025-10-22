# Comment contribuer à l'Atlas des Qubits Biologiques

Merci de votre intérêt pour ce projet ! Chaque contribution aide à construire une ressource plus complète pour la communauté.

## 🎯 Périmètre des contributions

Nous acceptons principalement les **nouvelles entrées** pour le dataset `biological_qubits.csv`. Avant de proposer une nouvelle entrée, veuillez vous assurer qu'elle respecte le périmètre du projet (voir `README.md`).

En résumé, nous incluons :
- ✅ Systèmes bio-compatibles fonctionnant à température ambiante/physiologique.
- ✅ Démonstrations in vitro, in cellulo, ou in vivo.
- ✅ Systèmes d'hyperpolarisation avec application biologique.
- ✅ Candidats mécanistiques avec publication primaire (Classe D).

## ✨ Proposer une nouvelle entrée

La méthode préférée est d'ouvrir une **Issue** en utilisant le template "Nouvelle entrée de données".

### Checklist pour une nouvelle entrée

Avant de soumettre, veuillez vérifier les points suivants :

1.  **[ ] Publication source** : Une publication primaire avec un DOI valide est obligatoire.
2.  **[ ] Pas de doublon** : Le système n'est pas déjà présent dans le dataset.
3.  **[ ] Données extraites** : Toutes les colonnes pertinentes du schéma v1.2 sont remplies (ou marquées `NA` si non applicable).
4.  **[ ] Unités normalisées** : Les unités respectent la politique stricte du projet (voir `README.md`) :
    - `Temperature_K` : en Kelvin (K)
    - `T2_us` : en microsecondes (µs)
    - `T1_s` : en secondes (s)
    - `B0_Tesla` : en Tesla (T)
    - `Contraste_%` : en pourcentage (%)
5.  **[ ] Provenance** : Si possible, renseignez les colonnes `Source_T1`, `Source_T2`, `Source_Contraste` avec le format `DOI:xxx Fig.X` ou `DOI:xxx Table S1`.
6.  **[ ] Statut de vérification** : Mettez `Verification_statut` à `a_confirmer`. L'équipe de maintenance le passera à `verifie` après validation.

### Modèle de soumission (format CSV)

Veuillez fournir les données sous forme de ligne CSV, que vous pouvez coller dans le corps de l'issue.

```csv
"Mon nouveau système",B,"Cellules HEK293",ODMR,"2.87 GHz","0.005","Electron","NV-","NA","NA","0.003","1.5","15",310,"80","λex=532nm; λem=650-800nm","Conditions spécifiques...","Limitations connues...",1,"10.1234/science.abc1234",2025,2,"a_confirmer","Notes additionnelles...","DOI:10.1234/science.abc1234 Fig. 2c","DOI:10.1234/science.abc1234 text","DOI:10.1234/science.abc1234 Fig. 2d","0.1","0.0005","1.2",0,0,"NA",1
```

## 🐛 Rapporter un bug ou une erreur

Si vous trouvez une erreur dans le dataset ou un bug dans l'interface web, veuillez ouvrir une issue en utilisant le template "Rapport de bug".

## Code de conduite

Ce projet adhère à un code de conduite. En participant, vous vous engagez à le respecter.
