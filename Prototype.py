
# ==================================================
# FICHIER : Prototype.py
# ROLE : Contenir toutes les classes du projet
# ==================================================


# ==================================================
# 1. CLASSE VEHICULE
# ==================================================

class Vehicule:

    # La méthode __init__ est appelée automatiquement
    # lorsqu'on crée un nouvel objet Vehicule.
    def __init__(self, id, marque, modele, tarif_journalier):

        # Vérifier que le tarif est supérieur à zéro
        if tarif_journalier <= 0:
            raise ValueError("Le tarif doit être supérieur à zéro.")

        # Les attributs représentent les informations du véhicule
        self.id = id
        self.marque = marque
        self.modele = modele

        # Le caractère "_" indique que cet attribut est privé
        # par convention : on évite de le modifier directement.
        self._tarif_journalier = tarif_journalier

        # État initial du véhicule
        self.etat = "disponible"

    # ==============================================
    # ENCAPSULATION DU TARIF
    # ==============================================

    @property
    def tarif_journalier(self):

        # @property permet de lire une méthode
        # comme s'il s'agissait d'un attribut.
        return self._tarif_journalier

    @tarif_journalier.setter
    def tarif_journalier(self, valeur):

        # @setter permet de contrôler la modification
        # de la valeur de notre attribut.
        if valeur <= 0:
            raise ValueError("Tarif invalide.")

        self._tarif_journalier = valeur

    # ==============================================
    # CALCULER LE TARIF
    # ==============================================

    def calculer_tarif(self, nombre_jours):

        # Multiplier le tarif journalier par le nombre de jours
        montant = self.tarif_journalier * nombre_jours

        return montant

    # ==============================================
    # AFFICHER LES INFORMATIONS
    # ==============================================

    def afficher_informations(self):

        print(f"ID : {self.id}")
        print(f"Marque : {self.marque}")
        print(f"Modèle : {self.modele}")
        print(f"Tarif : {self.tarif_journalier} $")
        print(f"État : {self.etat}")


# ==================================================
# 2. CLASSE VOITURE
# ==================================================

# Voiture hérite de Vehicule.
# Cela signifie qu'elle récupère ses attributs et ses méthodes.

class Voiture(Vehicule):

    def __init__(self, id, marque, modele, tarif_journalier, nombre_places):

        # super() permet d'appeler le constructeur de la classe parent.
        # Ici, on initialise les informations communes du véhicule.
        super().__init__(id, marque, modele, tarif_journalier)

        # Ajouter une information propre à la voiture
        self.nombre_places = nombre_places

    def afficher_informations(self):

        # Afficher d'abord les informations héritées de Vehicule
        super().afficher_informations()

        # Afficher ensuite le nombre de places
        print(f"Nombre de places : {self.nombre_places}")


# ==================================================
# 3. CLASSE MOTO
# ==================================================

class Moto(Vehicule):

    def __init__(self, id, marque, modele, tarif_journalier, cylindree):

        # Récupérer les informations communes de Vehicule
        super().__init__(id, marque, modele, tarif_journalier)

        # Ajouter une information propre à la moto
        self.cylindree = cylindree

    def afficher_informations(self):

        # Afficher les informations communes du véhicule
        super().afficher_informations()

        # Afficher la cylindrée de la moto
        print(f"Cylindrée : {self.cylindree} cc")


# ==================================================
# 4. CLASSE CLIENT
# ==================================================

class Client:

    def __init__(self, id_client, nom, prenom, telephone, adresse):

        # Informations personnelles du client
        self.id_client = id_client
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.adresse = adresse

    def afficher_informations(self):

        print(f"ID : {self.id_client}")
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Téléphone : {self.telephone}")
        print(f"Adresse : {self.adresse}")


# ==================================================
# 5. CLASSE RESERVATION
# ==================================================

class Reservation:

    def __init__(self, id_reservation, client, vehicule,
                 date_debut, date_fin):

        # Informations principales de la réservation
        self.id_reservation = id_reservation
        self.client = client
        self.vehicule = vehicule
        self.date_debut = date_debut
        self.date_fin = date_fin

        # Une nouvelle réservation est confirmée par défaut
        self.statut = "Confirmée"

        # Informations qui seront complétées plus tard
        self.date_depart_reelle = None
        self.date_retour_reelle = None

        # Nombre de jours de retard
        self.jours_retard = 0

        # Montant total de la réservation
        self.montant_total = 0


# ==================================================
# 6. CLASSE MAINTENANCE
# ==================================================

class Maintenance:

    def __init__(self, id_maintenance, vehicule,
                 date_debut, date_fin, motif):

        # Informations de la maintenance
        self.id_maintenance = id_maintenance
        self.vehicule = vehicule
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.motif = motif

        # Une maintenance est planifiée au départ
        self.statut = "Planifiée"


# ==================================================
# 7. CLASSE HISTORIQUE
# ==================================================

class Historique:

    def __init__(self, id_historique, action,
                 description, date_operation):

        # Informations sur chaque opération effectuée
        self.id_historique = id_historique
        self.action = action
        self.description = description
        self.date_operation = date_operation
