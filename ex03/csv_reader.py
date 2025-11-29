import logging

logging.basicConfig(
    filename='erreurs.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CsvException(Exception):
    def __init__(self, message):
        super().__init__(message)
        logging.error(f"CsvException: {message}")

class FichierIntrouvableException(CsvException):
    def __init__(self, chemin):
        message = f"Le fichier '{chemin}' est introuvable."
        super().__init__(message)

class LigneInvalideException(CsvException):
    def __init__(self, ligne_num, raison):
        message = f"Ligne {ligne_num}: {raison}"
        super().__init__(message)

class PrixNegatifException(CsvException):
    def __init__(self, ligne_num, prix):
        message = f"Ligne {ligne_num}: Le prix ne peut pas être négatif ({prix})."
        super().__init__(message)

def charger_csv(chemin):
    try:
        with open(chemin, 'r', encoding='utf-8') as fichier:
            lignes = fichier.readlines()
    except FileNotFoundError:
        raise FichierIntrouvableException(chemin)
    
    articles = []
    
    for i, ligne in enumerate(lignes, start=1):
        ligne = ligne.strip()
        
        if not ligne:
            continue
        
        colonnes = ligne.split(';')
        
        if len(colonnes) != 3:
            raise LigneInvalideException(i, f"Format invalide. Attendu 3 colonnes, trouvé {len(colonnes)}.")
        
        id_article, nom, prix_str = colonnes
        
        if not id_article.strip():
            raise LigneInvalideException(i, "L'ID ne peut pas être vide.")
        
        if not nom.strip():
            raise LigneInvalideException(i, "Le nom ne peut pas être vide.")
        
        try:
            prix = float(prix_str)
        except ValueError:
            raise LigneInvalideException(i, f"Le prix '{prix_str}' n'est pas un nombre valide.")
        
        if prix < 0:
            raise PrixNegatifException(i, prix)
        
        articles.append({
            "id": id_article.strip(),
            "nom": nom.strip(),
            "prix": prix
        })
    
    logging.info(f"Fichier '{chemin}' chargé avec succès: {len(articles)} article(s).")
    return articles