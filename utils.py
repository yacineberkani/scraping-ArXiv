from __init__ import *

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