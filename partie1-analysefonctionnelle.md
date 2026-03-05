# Partie 1 – Analyse fonctionnelle

## Approche globale

Je décompose le problème en une suite logique d'étapes :

```
[Image de l'utilisateur] → [Chargement et vérification] → [Analyse des couleurs] → [Calcul des surfaces] → [Affichage des résultats]
```

**Étape 1 : Charger et vérifier l'image**
- L'utilisateur envoie son fichier image (JPEG/PNG)
- On vérifie que le fichier est correct et assez grand
- On garde l'image dans le projet

**Étape 2 : Analyser les couleurs**
- Le logiciel repère toutes les couleurs différentes dans l'image
- **Important** : les couleurs exactement identiques sont rares, donc on regroupe par proximité (tolérance)
- On fait la liste des couleurs uniques trouvées

**Étape 3 : Calculer les surfaces**
- On compte combien de pixels pour chaque couleur
- On transforme ça en longueur de fil nécessaire
- On applique les réglages choisis par l'utilisateur

**Étape 4 : Montrer les résultats**
- On prépare un rapport facile à lire
- L'utilisateur peut voir les résultats sur l'écran
- On peut exporter les données si besoin

---

## Modèle de données

### Comment les informations s'organisent
```
Projet ──── CouleursDetectees ──── Couleurs
     │             │
     │         EstimationsFil
     │
 Réglages
```

### Les informations qu'on garde

**Projet**
- `id` (numéro) : numéro unique du projet
- `nom` (texte) : nom donné par l'utilisateur
- `image` (texte) : endroit où l'image est sauvegardée
- `date` (date) : quand le projet a été créé
- `reglages_id` (numéro) : lien vers les réglages

**Couleur**
- `id` (numéro) : numéro unique
- `code` (texte) : code de la couleur (ex: "#FF0000")
- `nom` (texte) : nom facile à lire (ex: "Rouge")

**CouleurDetectee**
- `id` (numéro) : numéro unique
- `projet_id` (numéro) : à quel projet ça appartient
- `couleur_id` (numéro) : quelle couleur c'est
- `pixels` (numéro) : nombre de pixels de cette couleur
- `pourcentage` (nombre) : pourcentage de la surface totale

**EstimationFil**
- `id` (numéro) : numéro unique
- `couleur_detectee_id` (numéro) : lien vers la couleur détectée
- `reglages_id` (numéro) : quels réglages ont été utilisés
- `fil_metres` (nombre) : combien de mètres de fil il faut
- `marge_securite` (nombre) : pourcentage de marge ajoutée

**Réglages**
- `id` (numéro) : numéro unique
- `densite` (nombre) : points de broderie par cm²
- `type_fil` (texte) : quel type de fil (coton, polyester...)
- `conversion` (nombre) : coefficient pour convertir les pixels en mètres de fil (ex: 0.001 mètre par pixel)

### Règles à respecter
- Un projet doit avoir au moins une couleur
- Une surface ne peut pas être négative
- Le code couleur doit être valide
- Le total des pourcentages doit faire 100%  

---

## Problèmes qu'on pourrait rencontrer et solutions

### Problèmes techniques

**1. Qualité des images**
- *Problème* : Images trop petites, floues ou avec du bruit → résultats imprécis
- *Solutions* : 
  - Exiger une taille minimum (ex: 500x500 pixels)
  - Nettoyer l'image avant de l'analyser
  - Prévenir l'utilisateur si l'image n'est pas assez bonne

**2. Couleurs très similaires**
- *Problème* : Couleurs presque identiques (#FF0000 et #FF0100) → trop de couleurs différentes
- *Solutions* :
  - Regrouper les couleurs qui se ressemblent beaucoup
  - Limiter le nombre de couleurs (ex: maximum 256)
  - Laisser l'utilisateur regrouper manuellement si besoin

**3. Images très grandes**
- *Problème* : Temps d'analyse trop long (plus de 30 secondes)
- *Solutions* :
  - Réduire la taille de l'image avant l'analyse
  - Traiter l'image par petits morceaux
  - Montrer une barre de progression et permettre d'arrêter

**4. Précision des calculs**
- *Problème* : Différence entre les pixels et les vrais points de broderie
- *Solutions* :
  - Créer des tables de conversion selon chaque type de tissu (coton, soie, lin...)
  - Ajouter une marge de sécurité intelligente : +10% pour les tissus simples, +20% pour les tissus difficiles
  - Afficher clairement "Estimation : entre X et Y mètres de fil" pour être transparent
  - Proposer un mode "précision" où l'utilisateur peut ajuster manuellement les coefficients
  - Garder un historique des projets réels pour affiner les calculs avec le temps

**5. Détection du fond d'image**
- *Problème* : Le fond (souvent blanc) ne doit pas être brodé mais occupe beaucoup de surface
- *Solutions* :
  - Détecter automatiquement la couleur dominante en pourcentage (souvent le fond)
  - Proposer à l'utilisateur de confirmer/exclure cette couleur
  - Permettre de sélectionner manuellement la zone de fond
  - Ignorer par défaut les couleurs qui couvrent plus de 40% de l'image

### Problèmes pratiques

**6. Motifs compliqués**
- *Problème* : Dégradés, couleurs transparentes, motifs complexes
- *Solutions* :
  - Ignorer les très petites zones (moins de 1% de la surface)
  - Simplifier en zones de couleur uniforme
  - Mode "avancé" pour ceux qui veulent plus de contrôle

**7. Différents types de matériaux**
- *Problème* : Le fil et le tissu changent la quantité nécessaire
- *Solutions* :
  - Garder une liste des matériaux avec leurs caractéristiques
  - Appliquer des coefficients selon le type de matériel
  - Permettre de tester plusieurs options

---
