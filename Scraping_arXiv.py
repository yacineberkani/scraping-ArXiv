import pandas as pd
import arxiv
import requests
import os
from langdetect import detect
from tqdm import tqdm
import spacy


def extraire_mots_cles_fr(requete):
    """
    Fonction pour extraire les mots-clés à partir de la requête de l'utilisateur en français.
    
    Arguments :
        - requete : La requête de l'utilisateur
        
    Returns :
        - mots_cles_format : Les mots-clés formatés sous forme de chaîne de caractères
    """
    nlp = spacy.load("fr_core_news_sm")
    requete_utilisateur = requete.lower()
    doc = nlp(requete_utilisateur)
    mots_cles = []
    for token in doc:
        if (token.pos_ == "NOUN" and token.dep_ not in ["ROOT","obj"]) or \
           (token.pos_ == "ADV" ) or \
           (token.pos_ == "PRON" and token.dep_ != "dep") or \
           (token.dep_ == "ROOT" and token.pos_ not in ["NOUN","VERB"]) or \
           (token.pos_ == "ADJ" ) or \
           (token.pos_ == "PROPN" and token.dep_ in ["nmod","punct"]):
            if not token.is_stop and not token.is_punct and token.text.lower() not in ['article', 'articles']:
                mots_cles.append(token.text)
    mots_cles_format = ' '.join(mots_cles)
    return mots_cles_format

def extraire_mots_cles_en(requete):
    """
    Fonction pour extraire les mots-clés à partir de la requête de l'utilisateur en anglais.
    
    Arguments :
        - requete : La requête de l'utilisateur
        
    Returns :
        - mots_cles_format : Les mots-clés formatés sous forme de chaîne de caractères
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(requete)
    mots_cles = []
    for token in doc:
        if (token.pos_ == "NOUN" ) or  (token.dep_ == "punct") or \
           (token.pos_ == "ADV") or (token.dep_ == "pobj") or \
           (token.pos_ == "PROPN" and token.dep_ != "dep") or \
           (token.pos_ == "ADJ" ) :
            if not token.is_stop and not token.is_punct and token.text.lower() not in ['article', 'articles']:
                mots_cles.append(token.text)
    mots_cles_format = ' '.join(mots_cles)
    return mots_cles_format

def detect_language(text):
    """
    Fonction pour détecter la langue d'un texte donné.
    
    Arguments :
        - text : Le texte à analyser
        
    Returns :
        - 'français' si la langue détectée est le français, sinon 'anglais'
    """
    lang = detect(text)
    if lang == 'fr':
        return 'français'
    else:
        return 'anglais'
def telecharger_articles_arxiv(sujet, nb_resultats):
    """
    Télécharge les articles d'arXiv pour un sujet donné et les stocke dans un dossier.

    Arguments :
    sujet : str - Le sujet de recherche pour les articles.
    nb_resultats : int - Le nombre de résultats à télécharger.

    Retourne :
    pandas.DataFrame - Un DataFrame contenant les détails des articles téléchargés.
    """

    
    # Effectuer la recherche sur arXiv
    recherche = arxiv.Search(
      query=sujet,
      max_results=nb_resultats,
      sort_by=arxiv.SortCriterion.SubmittedDate,
      sort_order=arxiv.SortOrder.Descending
    )
     
    # Création du dossier pour stocker les PDF
    nom_dossier = f"{sujet.replace(' ', '-')}-{nb_resultats}"
    os.makedirs(nom_dossier, exist_ok=True)

    # Initialisation du compteur d'articles téléchargés
    nb_articles = 0

    # Initialisation de la liste pour stocker toutes les données
    toutes_les_donnees = []

    # Parcourir les résultats de la recherche avec tqdm pour la barre de progression
    for resultat in tqdm(recherche.results(), desc="Téléchargement en cours"):
        # Initialisation de la liste temporaire pour stocker les données de chaque article
        temp = ["", "", "", "", "", "", "", ""]
        temp[0] = resultat.title
        temp[1] = resultat.authors
        temp[2] = resultat.published
        temp[3] = resultat.pdf_url
        temp[4] = resultat.summary
        temp[5] = resultat.doi
        temp[6] = resultat.journal_ref
        temp[7] = resultat.categories

        # Vérifier s'il existe une URL PDF pour l'article
        url_pdf = resultat.pdf_url
        if url_pdf:
            # Téléchargement du PDF
            reponse = requests.get(url_pdf)
            if reponse.status_code == 200:
                # Nom du fichier PDF
                nom_fichier_pdf = os.path.join(nom_dossier, f"{resultat.entry_id.split('/')[-1]}.pdf")
                # Écriture du contenu dans le fichier PDF
                with open(nom_fichier_pdf, 'wb') as f:
                    f.write(reponse.content)
                nb_articles += 1
                #print(f"Téléchargé {nom_fichier_pdf}")
            else:
                print(f"Échec du téléchargement du PDF depuis {url_pdf}")
        else:
            print(f"Aucune URL PDF disponible pour {resultat.entry_id}")

        # Ajouter les données de l'article à la liste des données
        toutes_les_donnees.append(temp)

    # Créer un DataFrame pandas à partir de toutes les données
    noms_colonnes = ['Titre', 'Auteur', 'Date', 'URL', 'Résumé', 'DOI', 'Journal', 'Catégories']
    df = pd.DataFrame(toutes_les_donnees, columns=noms_colonnes)
    
    # Enregistrer les données dans un fichier CSV avec le nom du dossier
    chemin_fichier_csv = os.path.join(nom_dossier, f"{nom_dossier}.csv")
    df.to_csv(chemin_fichier_csv, index=False)

    # Afficher le nombre total d'articles extraits
    #print("Nombre d'articles extraits : ", df.shape[0])

    # Afficher le nombre d'articles téléchargés
    print("Nombre d'articles téléchargés : ", nb_articles)

    # Retourner le DataFrame contenant les détails des articles téléchargés
    return print(df)

def main():
    """
    Fonction principale du programme.
    Demande à l'utilisateur le sujet de recherche, détecte la langue de la requête,
    extrait les mots-clés correspondants, demande le nombre de résultats à télécharger,
    télécharge les articles d'arXiv pour le sujet donné, les stocke dans un dossier
    et enregistre les détails des articles dans un fichier CSV.
    """
    # Demander à l'utilisateur le sujet de recherche
    requete_utilisateur = str(input("Veuillez saisir votre requête : "))

    # Détection de la langue de la requête
    langue = detect_language(requete_utilisateur)

    # Sélection de la fonction d'extraction des mots-clés en fonction de la langue détectée
    if langue == 'français':
        sujet = extraire_mots_cles_fr(requete_utilisateur)
        print("Langue détectée ==> Français")
    else:
        sujet = extraire_mots_cles_en(requete_utilisateur)
        print("Langue détectée ==> Anglais")
    
    # Demander à l'utilisateur le nombre de résultats à télécharger
    nb_resultats = int(input("Entrez le nombre de résultats : "))
    
    # Appeler la fonction de téléchargement des articles d'arXiv
    telecharger_articles_arxiv(sujet, nb_resultats)

if __name__ == "__main__":
    main()