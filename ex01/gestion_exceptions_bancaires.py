class TransactionException(Exception):
    def __init__(self, message):
        super().__init__(message)

class SoldeInsuffisantException(TransactionException):
    def __init__(self, message="Solde insuffisant pour ce retrait."):
        super().__init__(message)

class MontantNegatifException(TransactionException):
    def __init__(self, message="Le montant doit être positif."):
        super().__init__(message)

class MontantNulException(TransactionException):
    def __init__(self, message="Le montant ne peut pas être nul."):
        super().__init__(message)

class CompteBancaire:
    def __init__(self, nom, solde=0):
        self.nom = nom
        if solde < 0:
            raise MontantNegatifException("Le solde initial ne peut pas être négatif.")
        self.solde = solde

    def deposer(self, montant):
        if montant < 0:
            raise MontantNegatifException()
        if montant == 0:
            raise MontantNulException("Impossible de déposer 0€.")
        self.solde += montant

    def retirer(self, montant):
        if montant < 0:
            raise MontantNegatifException()
        if montant == 0:
            raise MontantNulException("Impossible de retirer 0€.")
        if montant > self.solde:
            raise SoldeInsuffisantException(f"Solde insuffisant. Vous avez {self.solde}€, tentative de retrait de {montant}€.")
        self.solde -= montant

    def afficher(self):
        print(f"Compte: {self.nom}, Solde: {self.solde}€")

if __name__ == "__main__":
    try:
        compte = CompteBancaire("Alice", 100)
        compte.afficher()
        
        compte.deposer(50)
        print("Dépôt de 50€ effectué")
        compte.afficher()
        
        compte.retirer(30)
        print("Retrait de 30€ effectué")
        compte.afficher()
        
        compte.retirer(150)
        
    except SoldeInsuffisantException as e:
        print(f"Erreur de solde: {e}")
    except MontantNegatifException as e:
        print(f"Erreur de montant: {e}")
    except MontantNulException as e:
        print(f"Erreur de montant: {e}")
    except TransactionException as e:
        print(f"Erreur de transaction: {e}")
    
    print("\n--- Test des exceptions ---")
    
    try:
        compte2 = CompteBancaire("Bob", 200)
        compte2.deposer(-50)
    except MontantNegatifException as e:
        print(f"Test dépôt négatif: {e}")
    
    try:
        compte2.deposer(0)
    except MontantNulException as e:
        print(f"Test dépôt nul: {e}")
    
    try:
        compte2.retirer(0)
    except MontantNulException as e:
        print(f"Test retrait nul: {e}")
    
    try:
        compte3 = CompteBancaire("Charlie", -100)
    except MontantNegatifException as e:
        print(f"Test solde initial négatif: {e}")