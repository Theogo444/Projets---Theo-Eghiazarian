# Fashion MNIST Classification - Deep Learning avec TensorFlow

## Description

Projet de Machine Learning implémentant un réseau de neurones profond (Deep Neural Network) pour la classification d'images de vêtements issues du dataset Fashion MNIST. Ce projet démontre l'utilisation de TensorFlow/Keras pour résoudre un problème de classification multi-classes sur des images en niveaux de gris. 

## Objectif

Développer un classificateur capable de reconnaître automatiquement 10 catégories différentes de vêtements et accessoires à partir d'images 28×28 pixels. Le projet illustre les étapes complètes d'un pipeline de Deep Learning : préparation des données, construction du modèle, entraînement, évaluation et prédiction.

## Dataset : Fashion MNIST

**Fashion MNIST** est un dataset de référence pour le Machine Learning, alternative moderne au MNIST classique. 

### Caractéristiques
- **Images** : 70,000 images en niveaux de gris (28×28 pixels) 
- **Entraînement** : 60,000 images 
- **Test** : 10,000 images 
- **Classes** : 10 catégories de vêtements

### Classes de vêtements
0. T-shirt/top
1. Trouser (Pantalon)
2. Pullover
3. Dress (Robe)
4. Coat (Manteau)
5. Sandal (Sandale)
6. Shirt (Chemise)
7. Sneaker (Basket)
8. Bag (Sac)
9. Ankle boot (Bottine)

## Architecture du modèle

### Réseau de neurones fully-connected

Le modèle utilise une architecture séquentielle simple mais efficace  : 

```python
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),    # Aplatissement 28×28 → 784
    keras.layers.Dense(300, activation="relu"),     # Couche cachée 1 : 300 neurones
    keras.layers.Dense(100, activation="relu"),     # Couche cachée 2 : 100 neurones
    keras.layers.Dense(10, activation="softmax")    # Couche de sortie : 10 classes
])
```

### Détail des couches

1. **Flatten** : Transforme les images 2D (28×28) en vecteurs 1D de 784 éléments 
2. **Dense(300, ReLU)** : Première couche cachée avec 235,500 paramètres
3. **Dense(100, ReLU)** : Deuxième couche cachée avec 30,100 paramètres 
4. **Dense(10, Softmax)** : Couche de sortie pour classification multi-classes avec 1,010 paramètres 

**Total** : 266,610 paramètres entraînables (1.02 MB) 

### Fonctions d'activation
- **ReLU** (Rectified Linear Unit) : Pour les couches cachées, introduit la non-linéarité 
- **Softmax** : Pour la couche de sortie, produit des probabilités sommant à 1 

## Prétraitement des données

### Normalisation
Les valeurs des pixels (0-255 en uint8) sont normalisées dans l'intervalle   :

```python
X_train = X_train_full[5000:] / 255.0
X_test = X_test / 255.0
```

### Split des données
- **Entraînement** : 55,000 images 
- **Validation** : 5,000 images 
- **Test** : 10,000 images 

## Compilation et entraînement

### Hyperparamètres

```python
model.compile(
    loss="sparse_categorical_crossentropy",  # Fonction de perte
    optimizer="sgd",                         # Optimiseur SGD
    metrics=["accuracy"]                     # Métrique d'évaluation
)
```

**Loss** : Sparse Categorical Crossentropy (labels entiers, pas one-hot) 
**Optimizer** : Stochastic Gradient Descent 
**Métrique** : Accuracy (précision de classification) 

### Entraînement

Le modèle est entraîné sur les données d'entraînement avec validation  : 

```python
history = model.fit(X_train, y_train, 
                    epochs=30, 
                    validation_data=(X_valid, y_valid))
```

## Résultats

Le projet génère :
- **Courbes d'apprentissage** : Évolution de la loss et accuracy sur les sets d'entraînement et validation 
- **Matrice de confusion** : Visualisation des erreurs de classification par classe
- **Exemples de prédictions** : Images test avec prédictions du modèle

### Performances attendues
- **Accuracy entraînement** : ~89-91%
- **Accuracy validation** : ~87-89%
- **Accuracy test** : ~87-89%

Les classes les plus confondues sont généralement Shirt/T-shirt/Pullover et Ankle boot/Sneaker en raison de leurs similarités visuelles.

## Technologies utilisées

- **Python 3.x**
- **TensorFlow 2.x** : Framework de Deep Learning 
- **Keras** : API haut niveau pour construction de réseaux de neurones 
- **NumPy** : Manipulation de tableaux numériques 
- **pandas** : Analyse de données 
- **matplotlib** : Visualisation des résultats et images 

## Utilisation

### Installation des dépendances

```bash
pip install tensorflow numpy pandas matplotlib
```

### Exécution du notebook

```bash
jupyter notebook MNIST_Fashion_tensorflow.ipynb
```

### Exemple de prédiction

```python
# Charger une image de test
import numpy as np

# Prédire sur une image
X_new = X_test[:3]
y_proba = model.predict(X_new)
y_pred = np.argmax(y_proba, axis=1)

# Afficher les prédictions
for i in range(3):
    print(f"Image {i}: {class_names[y_pred[i]]} (confiance: {y_proba[i][y_pred[i]]:.2%})")
```

## Améliorations possibles

### Optimisations du modèle
- **Régularisation** : Ajout de Dropout ou L2 pour réduire l'overfitting
- **Batch Normalization** : Stabilisation de l'entraînement
- **Optimiseurs avancés** : Adam, RMSprop au lieu de SGD
- **Learning rate scheduling** : Décroissance adaptative du taux d'apprentissage

### Architecture avancée
- **CNN (Convolutional Neural Networks)** : Meilleure performance sur images (accuracy ~92-94%)
- **Data Augmentation** : Rotation, zoom, shift pour augmenter la diversité des données
- **Transfer Learning** : Utilisation de modèles pré-entraînés

## Applications pratiques

- **E-commerce** : Classification automatique de produits vestimentaires
- **Systèmes de recommandation** : Suggestion de vêtements similaires
- **Recherche visuelle** : Recherche par image dans des catalogues
- **Contrôle qualité** : Détection d'anomalies dans la production textile
- **Introduction au Deep Learning** : Projet pédagogique pour comprendre les réseaux de neurones

## Contact

Pour plus d'informations sur ce projet, n'hésitez pas à me contacter via theo.eghiazarian@edhec.com ou https://www.linkedin.com/in/th%C3%A9o-eghiazarian-88623030b/

***

*Dernière mise à jour : Janvier 2026*

