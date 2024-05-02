from __init__ import *

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