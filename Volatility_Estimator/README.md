# Volatility Estimator - Comparaison des Estimateurs de Volatilité

## Description

Projet de finance quantitative comparant différentes méthodes d'estimation de la volatilité historique des actifs financiers. Ce projet explore quatre approches distinctes pour mesurer et prévoir la volatilité : la volatilité historique classique, les fenêtres glissantes (rolling window), la moyenne mobile exponentielle pondérée (EWMA) et les modèles GARCH. 

## Objectif

Développer et comparer plusieurs estimateurs de volatilité pour identifier la méthode la plus adaptée selon le contexte d'utilisation. Le projet permet d'analyser les forces et faiblesses de chaque approche en termes de réactivité, stabilité et capacité prédictive. 

## Méthodologies d'estimation

### 1. Volatilité Historique (Historic Volatility)

L'estimateur le plus simple, basé uniquement sur les rendements logarithmiques des prix de clôture  : 

$$\sigma_{hist} = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (r_i - \bar{r})^2} \times \sqrt{252}$$

où $r_i = \ln(C_i / C_{i-1})$

**Avantages** : Simple à calculer, intuitive, nécessite uniquement les prix de clôture 
**Inconvénients** : Tous les rendements ont le même poids, lente à réagir aux changements  
**Usage** : Benchmark de référence pour comparaison

### 2. Volatilité à Fenêtre Glissante (Rolling Window)

Calcul de la volatilité historique sur une fenêtre temporelle mobile (ex: 30, 60, 90 jours)  : 
$$\sigma_{roll,t} = \sqrt{\frac{1}{w-1} \sum_{i=t-w+1}^{t} (r_i - \bar{r})^2} \times \sqrt{252}$$

où $w$ est la taille de la fenêtre

**Avantages** : Capture l'évolution temporelle de la volatilité, adaptable via la taille de fenêtre 
**Inconvénients** : Effet "cliff" quand une observation sort de la fenêtre, choix arbitraire de $w$  
**Usage** : Analyse de tendances et régimes de volatilité

### 3. EWMA (Exponentially Weighted Moving Average)

Moyenne mobile exponentielle donnant plus de poids aux observations récentes  : 

$$\sigma_{EWMA,t}^2 = \lambda \sigma_{EWMA,t-1}^2 + (1-\lambda) r_{t-1}^2$$

où $\lambda$ est le facteur de décroissance (typiquement 0.94 pour données journalières selon RiskMetrics)

**Avantages** : Réagit rapidement aux chocs récents, poids décroissant continu, pas de paramètre de fenêtre 
**Inconvénients** : Sensible au choix de $\lambda$, pas de modélisation de la persistance  
**Usage** : Risk management, calcul de VaR en temps réel

### 4. Modèle GARCH(1,1)

Modélisation de la volatilité conditionnelle avec effet mémoire et clustering  : 
$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

où :
- $\omega$ : volatilité de long terme
- $\alpha$ : poids du choc récent (ARCH term)
- $\beta$ : persistance de la volatilité (GARCH term)
- $\alpha + \beta < 1$ pour la stationnarité

**Avantages** : Capture les clusters de volatilité, effet de persistance, prévision multi-périodes 
**Inconvénients** : Plus complexe, nécessite calibration, suppose symétrie des chocs  
**Usage** : Pricing d'options, prévision de volatilité, modélisation de risque

## Données utilisées

**Sources** : Yahoo Finance via `yfinance` 
**Actifs analysés** : Actions américaines (AAPL, GOOG, MSFT) 
**Période** : Janvier 2018 - Décembre 2025
**Fréquence** : Données journalières avec rendements logarithmiques 

## Technologies utilisées

- **Python 3.x**
- **NumPy** : Calculs numériques et statistiques 
- **pandas** : Manipulation de séries temporelles financières 
- **matplotlib** : Visualisations des volatilités 
- **Plotly** : Graphiques interactifs pour comparaisons 
- **yfinance** : Récupération de données de marché 
- **arch** : Estimation des modèles GARCH 

## Résultats et comparaison

### Comparaison des quatre méthodes

Le projet génère des visualisations comparant :
- **Évolution temporelle** : Superposition des volatilités estimées par chaque méthode
- **Réactivité** : Vitesse d'adaptation aux événements de marché (chocs, crashes)
- **Stabilité** : Variance et bruit dans les estimations
- **Prévision** : Capacité prédictive pour les périodes futures

### Observations clés

| Méthode | Réactivité | Stabilité | Prévision | Usage optimal |
|---------|------------|-----------|-----------|---------------|
| Historic Volatility | Faible | Élevée | Faible | Analyse long terme |
| Rolling Window | Moyenne | Moyenne | Moyenne | Analyse de régimes |
| EWMA | Élevée | Faible | Moyenne | Risk management temps réel |
| GARCH(1,1) | Adaptative | Moyenne | Élevée | Pricing et prévision |

### Insights pratiques

- **Historic volatility** : Stable mais lente, idéale pour contexte stable 
- **Rolling window** : Bon compromis, mais sensible au choix de fenêtre 
- **EWMA** : Très réactive, excellente pour détecter rapidement les changements de régime 
- **GARCH** : Meilleur modèle prédictif, capture la dynamique temporelle complexe 

## Utilisation

```python
# Installer les dépendances
pip install numpy pandas matplotlib plotly yfinance arch

# Exécuter le notebook
jupyter notebook Volatility_Estimator.ipynb
```

### Exemple de code

```python
import yfinance as yf
import numpy as np
from arch import arch_model

# Télécharger les données
data = yf.download('AAPL', start="2018-01-01", interval="1d")
data['log_returns'] = np.log(data['Close'] / data['Close'].shift(1))
data.dropna(inplace=True)

# 1. Volatilité historique
hist_vol = data['log_returns'].std() * np.sqrt(252)

# 2. Rolling window (30 jours)
roll_vol = data['log_returns'].rolling(30).std() * np.sqrt(252)

# 3. EWMA (lambda = 0.94)
ewma_vol = data['log_returns'].ewm(alpha=1-0.94).std() * np.sqrt(252)

# 4. GARCH(1,1)
model = arch_model(data['log_returns']*100, vol='Garch', p=1, q=1)
garch_fit = model.fit(disp='off')
garch_vol = garch_fit.conditional_volatility / 100 * np.sqrt(252)
```

## Applications pratiques

- **Trading d'options** : Calibration des modèles de pricing avec GARCH 
- **Risk management** : Calcul de VaR avec EWMA pour réactivité optimale 
- **Allocation d'actifs** : Optimisation de portefeuille selon les volatilités estimées
- **Backtesting** : Comparaison des performances prédictives des méthodes
- **Détection de régimes** : Identification de périodes haute/basse volatilité

## Contact

Pour plus d'informations sur ce projet, n'hésitez pas à me contacter via theo.eghiazarian@edhec.com ou https://www.linkedin.com/in/th%C3%A9o-eghiazarian-88623030b/

***

*Dernière mise à jour : Janvier 2026*
