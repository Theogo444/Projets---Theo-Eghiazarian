# Volatility Estimator - Comparaison des Estimateurs de Volatilité

## Description

Projet de finance quantitative comparant différentes méthodes d'estimation de la volatilité historique des actifs financiers. Ce projet explore les avantages des estimateurs utilisant les prix OHLC (Open, High, Low, Close) par rapport à l'estimateur classique basé uniquement sur les prix de clôture. 

## Objectif

Développer et comparer plusieurs estimateurs de volatilité pour démontrer que les méthodes utilisant l'information intraday (High-Low) sont plus efficaces que la volatilité historique simple. Le projet permet d'identifier l'estimateur le plus adapté selon le contexte et les données disponibles. 

## Méthodologies d'estimation

### 1. Volatilité historique classique (Close-to-Close)

L'estimateur le plus simple, basé uniquement sur les rendements logarithmiques des prix de clôture  : 

$$\sigma_{CC} = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (r_i - \bar{r})^2}$$

où $r_i = \ln(C_i / C_{i-1})$

**Avantages** : Simple, nécessite uniquement les prix de clôture  
**Inconvénients** : Ignore l'information intraday, moins efficace

### 2. Estimateur de Parkinson (High-Low)

Utilise l'amplitude High-Low pour capturer la volatilité intraday  : 
$$\sigma_{P} = \sqrt{\frac{1}{4n\ln(2)} \sum_{i=1}^{n} [\ln(H_i/L_i)]^2}$$

**Efficacité** : ~5 fois plus efficace que Close-to-Close  
**Hypothèse** : Pas de drift, pas de gap d'ouverture

### 3. Estimateur de Garman-Klass

Améliore Parkinson en intégrant les prix d'ouverture et de clôture  :
$$\sigma_{GK} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} \left[0.5[\ln(H_i/L_i)]^2 - (2\ln2-1)[\ln(C_i/O_i)]^2\right]}$$

**Efficacité** : ~7-8 fois plus efficace que Close-to-Close  
**Hypothèse** : Marchés continus (pas de gap)

### 4. Estimateur de Rogers-Satchell

Robuste en présence de drift, ne nécessite pas l'hypothèse de moyenne nulle  : 
$$\sigma_{RS} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} [\ln(H_i/C_i)\ln(H_i/O_i) + \ln(L_i/C_i)\ln(L_i/O_i)]}$$

**Avantage** : Résistant au drift des prix  
**Hypothèse** : Pas de gap d'ouverture

### 5. Estimateur de Yang-Zhang

Le plus complet, gère à la fois le drift et les gaps d'ouverture  : 

Combine la volatilité overnight, open-to-close, et Rogers-Satchell avec des poids optimaux.

**Efficacité** : ~14 fois plus efficace que Close-to-Close  
**Avantage** : Aucune restriction, le plus robuste

### 6. Modèle GARCH(1,1)

Modélisation de la volatilité conditionnelle avec effet mémoire  : 

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

**Avantage** : Capture les clusters de volatilité et l'effet de persistance

## Données utilisées

**Sources** : Yahoo Finance via `yfinance` 
**Actifs analysés** : Actions américaines (AAPL, GOOG, MSFT)  
**Période** : Janvier 2018 - Décembre 2025  
**Fréquence** : Données journalières avec prix OHLC

## Technologies utilisées

- **Python 3.x**
- **NumPy** : Calculs numériques et statistiques
- **pandas** : Manipulation de séries temporelles financières 
- **matplotlib** : Visualisations des volatilités
- **Plotly** : Graphiques interactifs pour comparaisons 
- **yfinance** : Récupération de données de marché 
- **arch** : Modèles GARCH pour volatilité conditionnelle 

## Résultats et insights

### Comparaison des estimateurs

Le projet génère des visualisations comparant :
- **Évolution temporelle** : Volatilités roulantes sur différentes fenêtres (30, 60, 90 jours)
- **Réactivité** : Vitesse d'adaptation aux chocs de marché
- **Efficacité** : Variance des estimations pour un même niveau de volatilité réelle

### Observations clés

- Les estimateurs High-Low (Parkinson, Garman-Klass) sont significativement plus efficaces que Close-to-Close [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/137473217/3c0c31f2-c26d-4ae1-a9f1-edce1c1310e5/Volatility_Estimator.ipynb)
- Yang-Zhang offre le meilleur compromis précision/robustesse pour tous types de marchés
- GARCH capture mieux les clusters de volatilité et la persistance temporelle
- L'estimateur optimal dépend des caractéristiques du sous-jacent (gaps, drift)

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

# Télécharger les données
data = yf.download('AAPL', start="2018-01-01", interval="1d")

# Calculer l'estimateur de Parkinson
def parkinson_volatility(data, window=30):
    hl = np.log(data['High'] / data['Low'])
    return np.sqrt((1/(4*np.log(2))) * (hl**2).rolling(window).mean()) * np.sqrt(252)

vol_parkinson = parkinson_volatility(data)
```

## Applications pratiques

- **Trading d'options** : Calibration des modèles de pricing (Black-Scholes)
- **Risk management** : Calcul de VaR et stress testing
- **Allocation d'actifs** : Optimisation de portefeuille selon Markowitz
- **Market making** : Ajustement des spreads selon la volatilité intraday
- **Stratégies de volatilité** : Trading de straddles, strangles basé sur les estimations

## Références théoriques

- **Parkinson (1980)** : "The Extreme Value Method for Estimating the Variance of the Rate of Return"
- **Garman & Klass (1980)** : "On the Estimation of Security Price Volatilities from Historical Data"
- **Rogers & Satchell (1991)** : "Estimating Variance from High, Low and Closing Prices"
- **Yang & Zhang (2000)** : "Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices"

## Contact

Pour plus d'informations sur ce projet, n'hésitez pas à me contacter via theo.eghiazarian@edhec.com ou https://www.linkedin.com/in/th%C3%A9o-eghiazarian-88623030b/

***

*Dernière mise à jour : Janvier 2026*
