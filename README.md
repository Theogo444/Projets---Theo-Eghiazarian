# Protfolio - Théo Eghiazarian

Ce portfolio regroupe plusieurs projets de data science, de finance quantitative et de machine learning couvrant un spectre allant de la modélisation de volatilité au deep learning sur images et à la data science sportive NBA .  

***

## Objet du repository

Ce repo général a pour but de présenter, dans un seul endroit, l’ensemble des projets réalisés autour :  
- de la **finance quantitative** (pricing, volatilité, gestion des risques)  
- du **machine learning supervisé** (régression, classification)  
- du **deep learning** (réseaux de neurones, TensorFlow)  
- de la **data science appliquée au sport** (NBA, salaires, performances) .  

Chaque dossier correspond à un projet autonome avec son propre notebook, ses données et un README détaillé.

***

## Structure des projets

### 1. Monte Carlo Pricing (Options)

Projet de **pricing d’options** via simulations de Monte Carlo sous hypothèse de Black‑Scholes.  
- Pricing d’options : européennes, asiatiques, barrières, lookback  
- Génération de trajectoires de prix, calcul de payoffs et actualisation  
- Techniques de réduction de variance (variables antithétiques, variable de contrôle)  
- Comparaison des prix simulés à des formules fermées quand elles existent. 

Technos : Python, NumPy, pandas, SciPy, matplotlib, Plotly, yfinance. 
***

### 2. Volatility Estimator

Projet d’**estimation et de comparaison de la volatilité** de marchés actions.  
Méthodes utilisées :  
- Volatilité historique (close‑to‑close)  
- Rolling window (volatilité glissante)  
- EWMA (Exponentially Weighted Moving Average)  
- GARCH(1,1) pour la volatilité conditionnelle. 

Données : séries quotidiennes de plusieurs actions US sur plusieurs années via yfinance. 
Objectif : comparer réactivité, stabilité et pouvoir prédictif des différents estimateurs. 

***

### 3. Fashion MNIST – TensorFlow

Projet de **classification d’images de vêtements** avec le dataset Fashion MNIST.  
- Dataset : 70 000 images 28×28 niveaux de gris, 10 classes (T‑shirt, sneaker, bag, etc.)  
- Modèle : réseau de neurones fully‑connected (Flatten → Dense 300 ReLU → Dense 100 ReLU → Dense 10 Softmax)  
- Pipeline : normalisation des pixels, split train/validation/test, entraînement, suivi des courbes de loss/accuracy. 

Technos : TensorFlow, Keras, NumPy, pandas, matplotlib. 

***

### 4. Volatilité – GARCH, EWMA & Rolling

Projet consacré aux **méthodes de prévision de volatilité** utilisées en risk management.  
- Implémentation détaillée de :  
  - Volatilité historique annualisée  
  - Fenêtres glissantes (plusieurs horizons)  
  - EWMA avec facteur de décroissance type RiskMetrics  
  - Modèles GARCH via la librairie `arch`. 
- Comparaison sur données réelles : impact sur VaR, réactivité aux chocs, persistance de la volatilité. 

***

### 5. NBA Salary Prediction (NPS Project)

Projet de **prédiction des salaires NBA** en fonction des performances des joueurs.  
Pipeline complet :  
- **Data gathering**  
  - Utilisation de l’API officielle NBA (`nba_api`) pour récupérer les stats par joueur et par saison (PPG, RPG, APG, SPG, BPG, FG%, FT%, 3PT, turnovers, fautes, minutes, âge, équipe, etc.)  
  - Contournement des limites de l’API via batchs, pauses entre requêtes et sauvegarde en ~25 CSV. 
- **Données financières**  
  - CSV de salaires et de salary cap par saison, calcul du ratio salaire / salary cap. 
- **Préprocessing / Feature engineering**  
  - Filtrage des joueurs à partir de 2000‑01, suppression des saisons incomplètes, gestion des joueurs transférés (ligne TOT uniquement), suppression des profils avec stats quasi nulles. 
- **Modélisation**  
  - Régressions (Linear, Ridge, Lasso), Decision Tree, Random Forest, SVR  
  - Pipelines scikit‑learn (StandardScaler, OneHotEncoder, imputation)  
  - Validation croisée groupée par joueur (GroupKFold / GroupShuffleSplit)  
  - Optimisation via GridSearchCV, métriques R² et MAE. 

Objectif : comprendre les déterminants d’un contrat NBA (PPG, usage, efficacité, âge, disponibilité, contexte salarial). 

***

## Stack technique globale

Sur l’ensemble du repo, les technologies principales sont :  
- **Python 3.x**  
- **Data / Stats** : pandas, NumPy, SciPy, statsmodels  
- **ML / DL** : scikit‑learn, TensorFlow / Keras, arch (GARCH)  
- **Visualisation** : matplotlib, seaborn, Plotly  
- **Données marché & sport** : yfinance, nba_api. 

***

## Comment utiliser ce repo

1. Cloner le repo :  
   ```bash
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```  
2. Créer un environnement et installer les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```  
3. Pour chaque projet, ouvrir le notebook correspondant (par ex. `Monte_Carlo_Pricing.ipynb`, `Volatility_Estimator.ipynb`, `MNIST_Fashion_tensorflow.ipynb`, `main.ipynb` pour le NPS Project) et suivre les étapes décrites dans son README dédié. 

***

## Contact
Mail : theo.eghiazarian@edhec.com
LinkedIn : https://www.linkedin.com/in/th%C3%A9o-eghiazarian-88623030b/
