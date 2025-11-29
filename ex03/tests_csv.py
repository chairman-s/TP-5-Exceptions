import unittest
import os
from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException
)

class TestCsvReader(unittest.TestCase):
    
    def setUp(self):
        self.fichier_valide = "test_valide.csv"
        self.fichier_prix_negatif = "test_prix_negatif.csv"
        self.fichier_prix_invalide = "test_prix_invalide.csv"
        self.fichier_colonnes_manquantes = "test_colonnes_manquantes.csv"
        self.fichier_vide = "test_vide.csv"
        
        with open(self.fichier_valide, 'w', encoding='utf-8') as f:
            f.write("1;Ordinateur;999.99\n")
            f.write("2;Souris;25.50\n")
            f.write("\n")
            f.write("3;Clavier;45.00\n")
        
        with open(self.fichier_prix_negatif, 'w', encoding='utf-8') as f:
            f.write("1;Article;-10.00\n")
        
        with open(self.fichier_prix_invalide, 'w', encoding='utf-8') as f:
            f.write("1;Article;abc\n")
        
        with open(self.fichier_colonnes_manquantes, 'w', encoding='utf-8') as f:
            f.write("1;ArticleSansLePrix\n")
        
        with open(self.fichier_vide, 'w', encoding='utf-8') as f:
            f.write("\n\n\n")
    
    def tearDown(self):
        fichiers = [
            self.fichier_valide,
            self.fichier_prix_negatif,
            self.fichier_prix_invalide,
            self.fichier_colonnes_manquantes,
            self.fichier_vide
        ]
        for fichier in fichiers:
            if os.path.exists(fichier):
                os.remove(fichier)
    
    def test_fichier_valide(self):
        articles = charger_csv(self.fichier_valide)
        self.assertEqual(len(articles), 3)
        self.assertEqual(articles[0]['id'], '1')
        self.assertEqual(articles[0]['nom'], 'Ordinateur')
        self.assertEqual(articles[0]['prix'], 999.99)
    
    def test_fichier_introuvable(self):
        with self.assertRaises(FichierIntrouvableException):
            charger_csv("fichier_qui_nexiste_pas.csv")
    
    def test_prix_negatif(self):
        with self.assertRaises(PrixNegatifException):
            charger_csv(self.fichier_prix_negatif)
    
    def test_prix_invalide(self):
        with self.assertRaises(LigneInvalideException):
            charger_csv(self.fichier_prix_invalide)
    
    def test_colonnes_manquantes(self):
        with self.assertRaises(LigneInvalideException):
            charger_csv(self.fichier_colonnes_manquantes)
    
    def test_fichier_vide(self):
        articles = charger_csv(self.fichier_vide)
        self.assertEqual(len(articles), 0)
    
    def test_lignes_vides_ignorees(self):
        articles = charger_csv(self.fichier_valide)
        self.assertEqual(len(articles), 3)

if __name__ == "__main__":
    unittest.main()