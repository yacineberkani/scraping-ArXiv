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