# ArXiv Article Downloader

Ce programme permet de télécharger des articles de la plateforme arXiv en fonction d'une requête spécifiée par l'utilisateur.

## Prérequis

Avant d'utiliser ce programme, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x
- Les bibliothèques Python suivantes :
  - pandas
  - arxiv
  - requests
  - spacy
  - langdetect
  - tqdm

## Installation des dépendances

Pour installer les dépendances, exécutez la commande suivante :
  ```
pip install -r requirements.txt
  ```

## Utilisation

1. Exécutez le script `main.py`.
2. Saisissez votre requête de recherche lorsque vous y êtes invité.
3. Indiquez le nombre d'articles que vous souhaitez télécharger.
4. Le programme téléchargera les articles correspondants et les enregistrera dans un dossier spécifique.

## Structure des fichiers

- `main.py` : Le script principal à exécuter pour utiliser le programme.
- `arxiv_article_downloader.py` : Le module contenant les fonctions de téléchargement des articles.
- `utils.py` : Le module contenant des fonctions utilitaires.
- `requirements.txt` : Fichier contenant la liste des dépendances à installer.

## Auteurs

Ce projet a été réalisé par BERAKNI Yacine.
