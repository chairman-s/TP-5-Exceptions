import logging
from datetime import datetime

logging.basicConfig(
    filename='reservations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ReservationException(Exception):
    def __init__(self, message):
        super().__init__(message)
        logging.error(f"ReservationException: {message}")

class CapaciteDepasseeException(ReservationException):
    def __init__(self, message="Capacité dépassée."):
        super().__init__(message)

class NombreInvalideException(ReservationException):
    def __init__(self, message="Nombre de places invalide."):
        super().__init__(message)

class NomClientInvalideException(ReservationException):
    def __init__(self, message="Nom du client requis."):
        super().__init__(message)

class Client:
    _compteur_id = 1
    
    def __init__(self, nom):
        self.id = Client._compteur_id
        Client._compteur_id += 1
        self.nom = nom
    
    def __str__(self):
        return f"Client #{self.id}: {self.nom}"

class Reservation:
    def __init__(self, client, nb_places, timestamp=None):
        self.client = client
        self.nb_places = nb_places
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self):
        return f"{self.client} - {self.nb_places} place(s) - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class Evenement:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite
        self.places_reservees = 0
        self.reservations = []
        self.file_attente = []
        logging.info(f"Événement créé: {nom} (capacité: {capacite})")

    def reserver(self, nom_client, nb_places):
        if not nom_client.strip():
            raise NomClientInvalideException()
        
        if nb_places <= 0:
            raise NombreInvalideException()
        
        if self.places_reservees + nb_places > self.capacite:
            client = Client(nom_client)
            self.file_attente.append((client, nb_places))
            logging.warning(f"Capacité dépassée. Client {nom_client} ajouté à la file d'attente ({nb_places} places)")
            raise CapaciteDepasseeException(f"Capacité dépassée. {nom_client} ajouté à la file d'attente.")

        client = Client(nom_client)
        reservation = Reservation(client, nb_places)
        self.reservations.append(reservation)
        self.places_reservees += nb_places
        
        logging.info(f"Réservation confirmée: {client} - {nb_places} place(s)")
        print(f"Réservation confirmée pour {nom_client} ({nb_places} places).")
        print(f"ID de réservation: {client.id}")

    def annuler_reservation(self, client_id):
        for i, reservation in enumerate(self.reservations):
            if reservation.client.id == client_id:
                self.places_reservees -= reservation.nb_places
                self.reservations.pop(i)
                logging.info(f"Annulation: Client #{client_id} - {reservation.nb_places} place(s) libérées")
                print(f"Réservation #{client_id} annulée. {reservation.nb_places} place(s) libérée(s).")
                
                self._traiter_file_attente()
                return
        
        print(f"Aucune réservation trouvée avec l'ID {client_id}")

    def _traiter_file_attente(self):
        while self.file_attente:
            client, nb_places = self.file_attente[0]
            if self.places_reservees + nb_places <= self.capacite:
                self.file_attente.pop(0)
                reservation = Reservation(client, nb_places)
                self.reservations.append(reservation)
                self.places_reservees += nb_places
                logging.info(f"File d'attente: Réservation confirmée pour {client} - {nb_places} place(s)")
                print(f"File d'attente: Réservation confirmée pour {client.nom} ({nb_places} places).")
            else:
                break

    def afficher(self):
        print(f"\nÉvénement: {self.nom} — {self.places_reservees}/{self.capacite} places réservées")
        if self.reservations:
            print("Réservations:")
            for res in self.reservations:
                print(f"  - {res}")
        if self.file_attente:
            print(f"File d'attente: {len(self.file_attente)} client(s)")
            for client, nb in self.file_attente:
                print(f"  - {client.nom}: {nb} place(s)")

if __name__ == "__main__":
    print("=== Test du système de réservation ===\n")
    
    try:
        event = Evenement("Concert", 5)
        
        event.reserver("Alice", 2)
        event.afficher()
        
        event.reserver("Bob", 3)
        event.afficher()
        
        print("\n--- Tentative de dépassement de capacité ---")
        event.reserver("Charlie", 2)
        
    except CapaciteDepasseeException as e:
        print(f"Erreur: {e}")
    except ReservationException as e:
        print(f"Erreur: {e}")
    
    event.afficher()
    
    print("\n--- Annulation d'une réservation ---")
    event.annuler_reservation(1)
    event.afficher()
    
    print("\n--- Tests des validations ---")
    
    try:
        event.reserver("", 2)
    except NomClientInvalideException as e:
        print(f"Test nom vide: {e}")
    
    try:
        event.reserver("David", 0)
    except NombreInvalideException as e:
        print(f"Test nombre invalide: {e}")
    
    try:
        event.reserver("Eva", -3)
    except NombreInvalideException as e:
        print(f"Test nombre négatif: {e}")
    
    event.afficher()