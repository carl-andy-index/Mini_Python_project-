
import json
import os

from datetime import datetime

from Prototype import (
    Vehicule,
    Voiture,
    Moto,
    Client,
    Reservation,
    Maintenance,
    Historique
)


class gestionLocation:

    # =====================================
    # INITIALISATION
    # =====================================

    def __init__(self, fichier="location_data.json"):

        # Listes qui contiennent les données de l'application
        self.vehicules = []
        self.clients = []
        self.reservations = []
        self.maintenances = []
        self.historique = []

        # Nom du fichier dans lequel les données seront sauvegardées
        self.fichier = fichier

        # Autorise ou bloque les sauvegardes
        self.sauvegarde_autorisee = True

        # Charger les anciennes données au démarrage
        self.charger_donnees()

    # =====================================
    # OUTILS
    # =====================================

    def convertir_date(self, date):
        # Transformer une date texte en véritable date Python
        return datetime.strptime(date, "%Y-%m-%d")

    def dates_valides(self, debut, fin):

        try:
            date_debut = self.convertir_date(debut)
            date_fin = self.convertir_date(fin)

            # La date de fin doit être après la date de début
            if date_fin > date_debut:
                return True

            return False

        except ValueError:
            # La date n'a pas le bon format
            return False

    def chevauchement(self, debut1, fin1, debut2, fin2):

        # Vérifier si deux périodes se croisent
        if debut1 < fin2 and debut2 < fin1:
            return True

        return False

    def enregistrer_historique(self, action, description):

        # Créer un nouvel identifiant
        identifiant = len(self.historique) + 1

        # Créer l'objet Historique
        historique = Historique(
            identifiant,
            action,
            description,
            datetime.now().isoformat(timespec="seconds")
        )

        self.historique.append(historique)

    def sauvegarder_apres_operation(self):

        # Sauvegarder les données après une opération
        self.sauvegarder_donnees()

    # =====================================
    # VEHICULES
    # =====================================

    def ajouter_vehicule(self, vehicule):

        # Vérifier si l'identifiant existe déjà
        for v in self.vehicules:

            if v.id == vehicule.id:
                print("Erreur : identifiant déjà utilisé.")
                return False

        # Ajouter le véhicule
        self.vehicules.append(vehicule)

        self.enregistrer_historique(
            "Ajout véhicule",
            f"Véhicule {vehicule.id}"
        )

        self.sauvegarder_apres_operation()

        print("Véhicule ajouté.")
        return True

    def afficher_vehicules(self):

        for v in self.vehicules:
            v.afficher_informations()
            print("--------------------")

    def rechercher_vehicules(
        self,
        marque = None,
        type_vehicule = None,
        tarif_max= None,
        places=None,
        date_debut=None,
        date_fin=None
    ):

        resultat = []

        for v in self.vehicules:

            # Filtrer selon la marque
            if marque is not None and marque != "":
                if marque.lower() not in v.marque.lower():
                    continue

            # Filtrer selon le type
            if type_vehicule == "voiture":
                if not isinstance(v, Voiture):
                    continue

            if type_vehicule == "moto":
                if not isinstance(v, Moto):
                    continue

            # Filtrer selon le tarif maximum
            if tarif_max is not None:
                if v.tarif_journalier > tarif_max:
                    continue

            # Filtrer selon le nombre de places
            if places is not None:

                if not isinstance(v, Voiture):
                    continue

                if v.nombre_places < places:
                    continue

            # Vérifier la disponibilité pendant la période demandée
            if date_debut is not None and date_fin is not None:

                disponible = self.est_disponible(
                    v,
                    date_debut,
                    date_fin
                )

                if not disponible:
                    continue

            resultat.append(v)

        return resultat

    def est_disponible(self, vehicule, debut, fin):

        # Vérifier d'abord si les dates sont correctes
        if not self.dates_valides(debut, fin):
            return False

        debut = self.convertir_date(debut)
        fin = self.convertir_date(fin)

        # Vérifier les réservations existantes
        for r in self.reservations:

            if r.vehicule.id == vehicule.id:

                if r.statut != "Annulée":

                    date_debut = self.convertir_date(r.date_debut)
                    date_fin = self.convertir_date(r.date_fin)

                    if self.chevauchement(
                        debut,
                        fin,
                        date_debut,
                        date_fin
                    ):
                        return False

        # Vérifier les périodes de maintenance
        for m in self.maintenances:

            if m.vehicule.id == vehicule.id:

                date_debut = self.convertir_date(m.date_debut)
                date_fin = self.convertir_date(m.date_fin)

                if self.chevauchement(
                    debut,
                    fin,
                    date_debut,
                    date_fin
                ):
                    return False

        return True

    # =====================================
    # CLIENTS
    # =====================================

    def ajouter_client(self, client):

        # Vérifier si le client existe déjà
        for c in self.clients:

            if c.id_client == client.id_client:
                print("Erreur : client déjà enregistré.")
                return False

        self.clients.append(client)

        self.enregistrer_historique(
            "Ajout client",
            f"Client {client.id_client}"
        )

        self.sauvegarder_apres_operation()

        print("Client ajouté.")
        return True

    def afficher_clients(self):

        for c in self.clients:
            c.afficher_informations()
            print("--------------------")

    # =====================================
    # RESERVATIONS
    # =====================================

    def ajouter_reservation(self, reservation):

        client = None
        vehicule = None

        # Rechercher le client dans la liste
        for c in self.clients:

            if c.id_client == reservation.client.id_client:
                client = c
                break

        # Rechercher le véhicule dans la liste
        for v in self.vehicules:

            if v.id == reservation.vehicule.id:
                vehicule = v
                break

        # Vérifier l'existence du client
        if client is None:
            print("Erreur : client introuvable.")
            return False

        # Vérifier l'existence du véhicule
        if vehicule is None:
            print("Erreur : véhicule introuvable.")
            return False

        # Vérifier les dates
        if not self.dates_valides(
            reservation.date_debut,
            reservation.date_fin
        ):
            print("Erreur : dates invalides.")
            return False

        # Vérifier si l'identifiant de réservation existe déjà
        for r in self.reservations:

            if r.id_reservation == reservation.id_reservation:
                print("Erreur : identifiant de réservation déjà utilisé.")
                return False

        # Vérifier la disponibilité du véhicule
        if not self.est_disponible(
            vehicule,
            reservation.date_debut,
            reservation.date_fin
        ):
            print("Erreur : véhicule indisponible pendant cette période.")
            return False

        # Utiliser les objets réellement enregistrés
        reservation.client = client
        reservation.vehicule = vehicule

        self.reservations.append(reservation)

        self.enregistrer_historique(
            "Réservation",
            f"Réservation {reservation.id_reservation}"
        )

        self.sauvegarder_apres_operation()

        print("Réservation enregistrée.")
        return True

    def annuler_reservation(self, id_reservation):

        for r in self.reservations:

            if r.id_reservation == id_reservation:

                # Seules les réservations confirmées ou en attente
                # peuvent être annulées
                if r.statut != "Confirmée" and r.statut != "En attente":
                    print("Annulation impossible.")
                    return False

                r.statut = "Annulée"

                self.enregistrer_historique(
                    "Annulation",
                    f"Réservation {id_reservation}"
                )

                self.sauvegarder_apres_operation()

                print("Réservation annulée.")
                return True

        print("Réservation introuvable.")
        return False

    def afficher_reservations(self):

        for r in self.reservations:

            print(
                f"ID : {r.id_reservation} | "
                f"Client : {r.client.nom} | "
                f"Véhicule : {r.vehicule.marque} | "
                f"Statut : {r.statut}"
            )

    # =====================================
    # DEPART ET RETOUR
    # =====================================

    def enregistrer_depart(self, id_reservation, date_depart):

        for r in self.reservations:

            if r.id_reservation == id_reservation:

                # Vérifier le statut de la réservation
                if r.statut != "Confirmée":
                    print("Cette réservation ne peut pas démarrer.")
                    return False

                # Vérifier le format et la cohérence des dates
                if not self.dates_valides(date_depart, r.date_fin):
                    print("Date de départ invalide.")
                    return False

                date_depart_convertie = self.convertir_date(date_depart)
                date_debut_reservation = self.convertir_date(r.date_debut)

                if date_depart_convertie < date_debut_reservation:
                    print("Départ avant la période réservée.")
                    return False

                # Vérifier si le véhicule est en maintenance
                for m in self.maintenances:

                    if m.vehicule.id == r.vehicule.id:

                        debut_maintenance = self.convertir_date(m.date_debut)
                        fin_maintenance = self.convertir_date(m.date_fin)

                        fin_reservation = self.convertir_date(r.date_fin)

                        if self.chevauchement(
                            date_depart_convertie,
                            fin_reservation,
                            debut_maintenance,
                            fin_maintenance
                        ):
                            print("Véhicule en maintenance.")
                            return False

                # Enregistrer le départ
                r.date_depart_reelle = date_depart
                r.statut = "En cours"
                r.vehicule.etat = "loué"

                self.enregistrer_historique(
                    "Départ",
                    f"Réservation {id_reservation}"
                )

                self.sauvegarder_apres_operation()

                print("Départ enregistré.")
                return True

        print("Réservation introuvable.")
        return False

    def enregistrer_retour(self, id_reservation, date_retour):

        for r in self.reservations:

            if r.id_reservation == id_reservation:

                if r.statut != "En cours":
                    print("Aucune location en cours.")
                    return False

                try:
                    depart = self.convertir_date(r.date_depart_reelle)
                    retour = self.convertir_date(date_retour)
                    fin_prevue = self.convertir_date(r.date_fin)

                except ValueError:
                    print("Date invalide.")
                    return False

                # Le retour ne peut pas précéder le départ
                if retour < depart:
                    print("Le retour précède le départ.")
                    return False

                # Calculer le nombre de jours de location
                jours = (retour - depart).days

                if jours == 0:
                    jours = 1

                # Calculer le retard
                retard = (retour - fin_prevue).days

                if retard < 0:
                    retard = 0

                # Calculer le montant de la location
                tarif = r.vehicule.tarif_journalier
                montant_location = jours * tarif

                # Pénalité de retard : 50 % du tarif par jour
                frais_retard = retard * tarif * 0.5

                total = montant_location + frais_retard

                # Mettre à jour les informations de la réservation
                r.date_retour_reelle = date_retour
                r.jours_retard = retard
                r.montant_total = total
                r.statut = "Terminée"

                # Le véhicule redevient disponible
                r.vehicule.etat = "disponible"

                self.enregistrer_historique(
                    "Retour",
                    f"Réservation {id_reservation}, total : {total} $"
                )

                self.sauvegarder_apres_operation()

                print("Retour enregistré.")
                print("Jours de retard :", retard)
                print("Montant à payer :", total, "$")

                return True

        print("Réservation introuvable.")
        return False

    # =====================================
    # MAINTENANCE
    # =====================================

    def ajouter_maintenance(self, maintenance):

        vehicule = None

        # Rechercher le véhicule concerné
        for v in self.vehicules:

            if v.id == maintenance.vehicule.id:
                vehicule = v
                break

        if vehicule is None:
            print("Véhicule introuvable.")
            return False

        # Vérifier les dates
        if not self.dates_valides(
            maintenance.date_debut,
            maintenance.date_fin
        ):
            print("Dates de maintenance invalides.")
            return False

        # Vérifier l'identifiant de maintenance
        for m in self.maintenances:

            if m.id_maintenance == maintenance.id_maintenance:
                print("Identifiant de maintenance déjà utilisé.")
                return False

        debut = self.convertir_date(maintenance.date_debut)
        fin = self.convertir_date(maintenance.date_fin)

        # Vérifier les réservations qui pourraient être concernées
        for r in self.reservations:

            if r.vehicule.id == vehicule.id:

                if r.statut != "Annulée" and r.statut != "Terminée":

                    date_debut = self.convertir_date(r.date_debut)
                    date_fin = self.convertir_date(r.date_fin)

                    if self.chevauchement(
                        debut,
                        fin,
                        date_debut,
                        date_fin
                    ):
                        print("Une réservation existe pendant cette période.")
                        return False

        # Vérifier les autres maintenances
        for m in self.maintenances:

            if m.vehicule.id == vehicule.id:

                date_debut = self.convertir_date(m.date_debut)
                date_fin = self.convertir_date(m.date_fin)

                if self.chevauchement(
                    debut,
                    fin,
                    date_debut,
                    date_fin
                ):
                    print("Une maintenance existe déjà.")
                    return False

        maintenance.vehicule = vehicule
        self.maintenances.append(maintenance)

        self.enregistrer_historique(
            "Maintenance",
            f"Maintenance {maintenance.id_maintenance}"
        )

        self.sauvegarder_apres_operation()

        print("Maintenance enregistrée.")
        return True

    # =====================================
    # STATISTIQUES
    # =====================================

    def afficher_statistiques(self):

        revenus = 0
        retards = 0
        frequences = {}

        # Calculer les revenus et les retards
        for r in self.reservations:

            revenus = revenus + r.montant_total

            if r.jours_retard > 0:
                retards = retards + 1

            # Compter uniquement les locations terminées
            if r.statut == "Terminée":

                identifiant = r.vehicule.id

                if identifiant in frequences:
                    frequences[identifiant] = frequences[identifiant] + 1
                else:
                    frequences[identifiant] = 1

        print("\n===== STATISTIQUES =====")
        print("Revenus :", revenus, "$")
        print("Réservations en retard :", retards)

        # Trouver le véhicule le plus loué
        if len(frequences) > 0:

            meilleur = None
            nombre_locations = 0

            for identifiant in frequences:

                if frequences[identifiant] > nombre_locations:
                    meilleur = identifiant
                    nombre_locations = frequences[identifiant]

            print("Véhicule le plus loué :", meilleur)
            print("Nombre de locations :", nombre_locations)

        else:
            print("Aucune location enregistrée.")

    def afficher_historique(self):

        for h in self.historique:

            print(
                h.date_operation,
                "|",
                h.action,
                "|",
                h.description
            )

    # =====================================
    # SAUVEGARDE JSON
    # =====================================

    def sauvegarder_donnees(self):

        if not self.sauvegarde_autorisee:
            raise RuntimeError(
                "Sauvegarde bloquée : le fichier JSON est invalide. "
                "Son contenu doit être vérifié manuellement."
            )

        # Préparer les catégories de données
        donnees = {
            "vehicules": [],
            "clients": [],
            "reservations": [],
            "maintenances": [],
            "historique": []
        }

        # Sauvegarder les véhicules
        for v in self.vehicules:

            element = {
                "id": v.id,
                "marque": v.marque,
                "modele": v.modele,
                "tarif": v.tarif_journalier,
                "etat": v.etat
            }

            if isinstance(v, Voiture):

                element["type"] = "Voiture"
                element["nombre_places"] = v.nombre_places

            elif isinstance(v, Moto):

                element["type"] = "Moto"
                element["cylindree"] = v.cylindree

            else:
                element["type"] = "Vehicule"

            donnees["vehicules"].append(element)

        # Sauvegarder les clients
        for c in self.clients:

            element = {
                "id": c.id_client,
                "nom": c.nom,
                "prenom": c.prenom,
                "telephone": c.telephone,
                "adresse": c.adresse
            }

            donnees["clients"].append(element)

        # Sauvegarder les réservations
        for r in self.reservations:

            element = {
                "id": r.id_reservation,
                "client_id": r.client.id_client,
                "vehicule_id": r.vehicule.id,
                "date_debut": r.date_debut,
                "date_fin": r.date_fin,
                "statut": r.statut,
                "depart": r.date_depart_reelle,
                "retour": r.date_retour_reelle,
                "retard": r.jours_retard,
                "montant": r.montant_total
            }

            donnees["reservations"].append(element)

        # Sauvegarder les maintenances
        for m in self.maintenances:

            element = {
                "id": m.id_maintenance,
                "vehicule_id": m.vehicule.id,
                "date_debut": m.date_debut,
                "date_fin": m.date_fin,
                "motif": m.motif,
                "statut": m.statut
            }

            donnees["maintenances"].append(element)

        # Sauvegarder l'historique
        for h in self.historique:

            element = {
                "id": h.id_historique,
                "action": h.action,
                "description": h.description,
                "date": h.date_operation
            }

            donnees["historique"].append(element)

        # Utiliser un fichier temporaire avant de remplacer le fichier principal
        temporaire = self.fichier + ".tmp"

        try:

            with open(temporaire, "w", encoding="utf-8") as f:

                json.dump(
                    donnees,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            # Remplacer le fichier principal par le fichier temporaire
            os.replace(temporaire, self.fichier)

        except Exception:

            # Supprimer le fichier temporaire en cas de problème
            if os.path.exists(temporaire):
                os.remove(temporaire)

            raise

    # =====================================
    # CHARGEMENT JSON
    # =====================================

    def charger_donnees(self):

        # Si le fichier n'existe pas encore, il n'y a rien à charger
        if not os.path.exists(self.fichier):
            return

        try:

            with open(self.fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)

            if not isinstance(donnees, dict):
                raise ValueError("Structure JSON invalide.")

            # Ces dictionnaires permettent de retrouver rapidement
            # un véhicule ou un client à partir de son identifiant
            vehicules = {}
            clients = {}

            # Charger les véhicules
            for element in donnees.get("vehicules", []):

                type_vehicule = element["type"]

                if type_vehicule == "Voiture":

                    v = Voiture(
                        element["id"],
                        element["marque"],
                        element["modele"],
                        element["tarif"],
                        element["nombre_places"]
                    )

                elif type_vehicule == "Moto":

                    v = Moto(
                        element["id"],
                        element["marque"],
                        element["modele"],
                        element["tarif"],
                        element["cylindree"]
                    )

                else:

                    v = Vehicule(
                        element["id"],
                        element["marque"],
                        element["modele"],
                        element["tarif"]
                    )

                v.etat = element.get("etat", "disponible")

                self.vehicules.append(v)

                vehicules[v.id] = v

            # Charger les clients
            for element in donnees.get("clients", []):

                c = Client(
                    element["id"],
                    element["nom"],
                    element["prenom"],
                    element["telephone"],
                    element["adresse"]
                )

                self.clients.append(c)

                clients[c.id_client] = c

            # Charger les réservations
            for element in donnees.get("reservations", []):

                r = Reservation(
                    element["id"],
                    clients[element["client_id"]],
                    vehicules[element["vehicule_id"]],
                    element["date_debut"],
                    element["date_fin"]
                )

                r.statut = element["statut"]
                r.date_depart_reelle = element.get("depart")
                r.date_retour_reelle = element.get("retour")
                r.jours_retard = element.get("retard", 0)
                r.montant_total = element.get("montant", 0)

                self.reservations.append(r)

            # Charger les maintenances
            for element in donnees.get("maintenances", []):

                m = Maintenance(
                    element["id"],
                    vehicules[element["vehicule_id"]],
                    element["date_debut"],
                    element["date_fin"],
                    element["motif"]
                )

                m.statut = element.get("statut", "Planifiée")

                self.maintenances.append(m)

            # Charger l'historique
            for element in donnees.get("historique", []):

                h = Historique(
                    element["id"],
                    element["action"],
                    element["description"],
                    element["date"]
                )

                self.historique.append(h)

            print("Données chargées avec succès.")

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
            OSError
        ) as erreur:

            # En cas de problème, vider les listes
            self.vehicules.clear()
            self.clients.clear()
            self.reservations.clear()
            self.maintenances.clear()
            self.historique.clear()

            # Empêcher l'écrasement du fichier JSON invalide
            self.sauvegarde_autorisee = False

            print("ERREUR : fichier JSON invalide.")
            print("Les données ne seront pas écrasées.")
            print(erreur)
