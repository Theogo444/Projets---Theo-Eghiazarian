#  Correlation Heatmap - Analyse Multi-Assets

## Description

Projet d'analyse quantitative visualisant les corrélations entre différentes classes d'actifs financiers (actions, indices, devises, matières premières et taux d'intérêt). Ce projet utilise des données historiques depuis 2020 pour identifier les relations entre actifs et leur évolution dans le temps. 

##  Objectif

Analyser et visualiser les corrélations entre divers instruments financiers pour comprendre leurs interdépendances et identifier les opportunités de diversification de portefeuille. Ce type d'analyse est essentiel en gestion de risque et construction de portefeuille. 

## Données utilisées

Les données sont récupérées via l'API Yahoo Finance (yfinance) couvrant la période de janvier 2020 à janvier 2026  : 

### Actions Tech (5 titres)
- **AAPL** (Apple), **MSFT** (Microsoft), **NVDA** (Nvidia), **TSLA** (Tesla), **AMZN** (Amazon)

### Indices boursiers (2 indices)
- **S&P 500** (^GSPC), **Nasdaq 100** (^NDX)

### Paires de devises (5 paires)
- **EUR/USD**, **USD/JPY**, **AUD/USD**, **GBP/USD**, **USD/CHF**

### Matières premières (4 commodités)
- **Or** (GC=F), **Pétrole** (CL=F), **Cuivre** (HG=F), **Argent** (SI=F)

### Taux d'intérêt US (3 maturités)
- **Taux 2 ans** (^IRX), **Taux 5 ans** (^FVX), **Taux 10 ans** (^TNX)

##  Méthodologie

1. **Récupération des données** : Téléchargement automatisé des prix de clôture via `yfinance` pour tous les actifs 
2. **Calcul des rendements** : Transformation des prix en rendements logarithmiques pour analyse statistique
3. **Matrices de corrélation** : Calcul des corrélations de Pearson entre les rendements des différents actifs
4. **Visualisation interactive** : Création de heatmaps avec Plotly pour explorer les relations entre actifs 
5. **Analyse temporelle** : Étude de l'évolution des corrélations sur différentes périodes (fenêtres glissantes)

##  Technologies utilisées

- **Python 3.x**
- **pandas** : Manipulation et analyse de données
- **NumPy** : Calculs numériques
- **yfinance** : Récupération de données financières
- **Plotly** : Visualisations interactives (graphiques et heatmaps) 
- **matplotlib** : Visualisations statiques complémentaires

##  Résultats clés

Le projet génère plusieurs visualisations permettant de :
- Identifier les actifs fortement corrélés (ex: actions tech entre elles)
- Détecter les actifs décorrélés pour la diversification
- Analyser l'impact des événements macroéconomiques sur les corrélations
- Comparer les comportements des différentes classes d'actifs

##  Utilisation

```python
# Installer les dépendances
pip install pandas numpy yfinance plotly matplotlib

# Exécuter le notebook
jupyter notebook Correlation_Heatmap.ipynb
```

##  Structure du projet

```
Correlation_Heatmap.ipynb    # Notebook principal avec analyses et visualisations
```

##  Applications pratiques

- **Gestion de portefeuille** : Optimisation de la diversification
- **Risk management** : Identification des risques systémiques
- **Trading quantitatif** : Détection de stratégies pairs trading
- **Analyse macroéconomique** : Étude des relations entre classes d'actifs

##  Contact

Pour plus d'informations sur ce projet, n'hésitez pas à me contacter via theo.eghiazarian@edhec.com ou https://www.linkedin.com/in/th%C3%A9o-eghiazarian-88623030b/.

***

*Dernière mise à jour : Janvier 2026*
