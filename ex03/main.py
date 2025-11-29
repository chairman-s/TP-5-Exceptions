from csv_reader import (
    charger_csv,
    CsvException,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException
)

def main():
    fichiers_test = [
        "articles_valides.csv",
        "articles_invalides.csv",
        "fichier_inexistant.csv"
    ]
    
    for fichier in fichiers_test:
        print(f"\n{'='*50}")
        print(f"Traitement du fichier: {fichier}")
        print('='*50)
        
        try:
            articles = charger_csv(fichier)
            print(f"✓ Succès: {len(articles)} article(s) chargé(s)\n")
            
            for article in articles:
                print(f"  • ID: {article['id']:<5} | Nom: {article['nom']:<20} | Prix: {article['prix']:.2f}€")
        
        except FichierIntrouvableException as e:
            print(f"✗ Erreur fichier: {e}")
        
        except PrixNegatifException as e:
            print(f"✗ Erreur prix: {e}")
        
        except LigneInvalideException as e:
            print(f"✗ Erreur format: {e}")
        
        except CsvException as e:
            print(f"✗ Erreur CSV: {e}")
        
        except Exception as e:
            print(f"✗ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()