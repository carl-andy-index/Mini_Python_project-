
# ==================================================
# FICHIER PRINCIPAL : main.py
# PROJET : GESTION DE LOCATION DE VEHICULES
# ==================================================


# Importer les classes depuis Prototype.py
from Prototype import Voiture, Moto, Client, Reservation, Maintenance

# Importer le gestionnaire de location
from Gestion_location import gestionLocation


# Créer notre gestionnaire
gestion = gestionLocation()


# ==================================================
# 1. OUTILS DE SAISIE
# ==================================================

def saisir_entier(message):

    while True:

        try:
            nombre = int(input(message))
            return nombre

        except ValueError:
            print("Veuillez entrer un nombre entier.")


def saisir_prix(message):

    while True:

        try:
            prix = float(input(message))

            if prix > 0:
                return prix

            else:
                print("Le prix doit être positif.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")


# ==================================================
# 2. RECHERCHER UN CLIENT
# ==================================================

def trouver_client(id_client):

    # Parcourir tous les clients enregistrés
    for client in gestion.clients:

        if client.id_client == id_client:
            return client

    # Si aucun client ne correspond à l'identifiant
    return None


# ==================================================
# 3. RECHERCHER UN VEHICULE
# ==================================================

def trouver_vehicule(id_vehicule):

    # Parcourir tous les véhicules enregistrés
    for vehicule in gestion.vehicules:

        if vehicule.id == id_vehicule:
            return vehicule

    # Si aucun véhicule ne correspond à l'identifiant
    return None


# ==================================================
# 4. AJOUTER UN VEHICULE
# ==================================================

def menu_ajouter_vehicule():

    print("\n1. Voiture")
    print("2. Moto")

    choix = input("Type de véhicule : ")

    identifiant = saisir_entier("ID : ")
    marque = input("Marque : ")
    modele = input("Modèle : ")
    tarif = saisir_prix("Tarif journalier : ")

    try:

        if choix == "1":

            places = saisir_entier("Nombre de places : ")

            if places <= 0:
                print("Nombre de places invalide.")
                return

            vehicule = Voiture(
                identifiant,
                marque,
                modele,
                tarif,
                places
            )

        elif choix == "2":

            cylindree = saisir_entier("Cylindrée : ")

            if cylindree <= 0:
                print("Cylindrée invalide.")
                return

            vehicule = Moto(
                identifiant,
                marque,
                modele,
                tarif,
                cylindree
            )

        else:
            print("Choix invalide.")
            return

        gestion.ajouter_vehicule(vehicule)

    except ValueError as erreur:
        print("Erreur :", erreur)


# ==================================================
# 5. AJOUTER UN CLIENT
# ==================================================

def menu_ajouter_client():

    identifiant = saisir_entier("ID client : ")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    telephone = input("Téléphone : ")
    adresse = input("Adresse : ")

    client = Client(
        identifiant,
        nom,
        prenom,
        telephone,
        adresse
    )

    gestion.ajouter_client(client)


# ==================================================
# 6. AJOUTER UNE RESERVATION
# ==================================================

def menu_ajouter_reservation():

    identifiant = saisir_entier("ID réservation : ")
    id_client = saisir_entier("ID client : ")
    id_vehicule = saisir_entier("ID véhicule : ")

    # Rechercher le client
    client = trouver_client(id_client)

    # Rechercher le véhicule
    vehicule = trouver_vehicule(id_vehicule)

    # Vérifier l'existence du client
    if client is None:
        print("Client introuvable.")
        return

    # Vérifier l'existence du véhicule
    if vehicule is None:
        print("Véhicule introuvable.")
        return

    debut = input("Date de début (AAAA-MM-JJ) : ")
    fin = input("Date de fin (AAAA-MM-JJ) : ")

    reservation = Reservation(
        identifiant,
        client,
        vehicule,
        debut,
        fin
    )

    gestion.ajouter_reservation(reservation)


# ==================================================
# 7. AJOUTER UNE MAINTENANCE
# ==================================================

def menu_maintenance():

    identifiant = saisir_entier("ID maintenance : ")
    id_vehicule = saisir_entier("ID véhicule : ")

    # Rechercher le véhicule concerné
    vehicule = trouver_vehicule(id_vehicule)

    if vehicule is None:
        print("Véhicule introuvable.")
        return

    debut = input("Date de début : ")
    fin = input("Date de fin : ")
    motif = input("Motif : ")

    maintenance = Maintenance(
        identifiant,
        vehicule,
        debut,
        fin,
        motif
    )

    gestion.ajouter_maintenance(maintenance)


# ==================================================
# 8. RECHERCHER DES VEHICULES
# ==================================================

def menu_rechercher_vehicule():

    marque = input("Marque (laisser vide pour toutes) : ")

    type_vehicule = input(
        "Type (voiture/moto/tous) : "
    ).lower()

    tarif = input(
        "Tarif maximum (laisser vide pour ignorer) : "
    )

    tarif_max = None

    if tarif != "":

        try:
            tarif_max = float(tarif)

            if tarif_max <= 0:
                print("Tarif invalide.")
                return

        except ValueError:
            print("Tarif invalide.")
            return

    debut = input("Date de début (vide pour ignorer) : ")
    fin = input("Date de fin (vide pour ignorer) : ")

    # Vérifier que les deux dates sont renseignées ensemble
    if debut == "" and fin != "":
        print("Veuillez saisir les deux dates.")
        return

    if debut != "" and fin == "":
        print("Veuillez saisir les deux dates.")
        return

    places = input(
        "Nombre minimum de places (vide pour ignorer) : "
    )

    places_min = None

    if places != "":

        try:
            places_min = int(places)

            if places_min <= 0:
                print("Nombre de places invalide.")
                return

        except ValueError:
            print("Nombre de places invalide.")
            return

    # Vérifier le type demandé
    if type_vehicule != "voiture" and type_vehicule != "moto":
        if type_vehicule != "tous" and type_vehicule != "":
            print("Type invalide.")
            return

    # Remplacer les champs vides par None.
    # None signifie ici que nous ne souhaitons pas utiliser ce critère.
    if marque == "":
        marque = None

    if type_vehicule == "tous" or type_vehicule == "":
        type_vehicule = None

    if debut == "":
        debut = None

    if fin == "":
        fin = None

    # Effectuer la recherche
    resultat = gestion.rechercher_vehicules(
        marque=marque,
        type_vehicule=type_vehicule,
        tarif_max=tarif_max,
        places=places_min,
        date_debut=debut,
        date_fin=fin
    )

    if not resultat:
        print("Aucun véhicule trouvé.")
        return

    # Trier les véhicules par tarif croissant
    for i in range(len(resultat)):

        for j in range(i + 1, len(resultat)):

            if resultat[i].tarif_journalier > resultat[j].tarif_journalier:

                temporaire = resultat[i]
                resultat[i] = resultat[j]
                resultat[j] = temporaire

    # Afficher les résultats
    for vehicule in resultat:

        vehicule.afficher_informations()
        print("--------------------")


# ==================================================
# 9. AFFICHER LE MENU PRINCIPAL
# ==================================================

def afficher_menu():

    print("\n========== LOCATION DE VEHICULES ==========")

    print(" 1.  Ajouter un véhicule")
    print(" 2.  Afficher les véhicules")
    print(" 3.  Ajouter un client")
    print(" 4.  Afficher les clients")
    print(" 5.  Ajouter une réservation")
    print(" 6.  Afficher les réservations")
    print(" 7.  Annuler une réservation")
    print(" 8.  Enregistrer un départ")
    print(" 9.  Enregistrer un retour")
    print(" 10. Ajouter une maintenance")
    print(" 11. Rechercher des véhicules")
    print(" 12. Afficher les statistiques")
    print(" 13. Consulter l'historique")
    print(" 0.  Quitter")

    print("===========================================\n")

    return input("Votre choix : ")


# ==================================================
# 10. PROGRAMME PRINCIPAL
# ==================================================

def main():

    # Vérifier si le fichier JSON permet les modifications
    if not gestion.sauvegarde_autorisee:

        print("\nAttention : fichier JSON invalide.")
        print("Mode lecture seule : aucune modification autorisée.")

    while True:

        choix = afficher_menu()

        # Quitter le programme
        if choix == "0":

            print("Fermeture de l'application.")
            break

        # Vérifier si les modifications sont autorisées
        if not gestion.sauvegarde_autorisee:

            print("Opération bloquée : vérifiez le fichier JSON.")
            continue

        try:

            if choix == "1":
                menu_ajouter_vehicule()

            elif choix == "2":
                gestion.afficher_vehicules()

            elif choix == "3":
                menu_ajouter_client()

            elif choix == "4":
                gestion.afficher_clients()

            elif choix == "5":
                menu_ajouter_reservation()

            elif choix == "6":
                gestion.afficher_reservations()

            elif choix == "7":

                identifiant = saisir_entier("ID réservation : ")

                gestion.annuler_reservation(identifiant)

            elif choix == "8":

                identifiant = saisir_entier("ID réservation : ")

                date = input(
                    "Date réelle de départ (AAAA-MM-JJ) : "
                )

                gestion.enregistrer_depart(identifiant, date)

            elif choix == "9":

                identifiant = saisir_entier("ID réservation : ")

                date = input(
                    "Date réelle de retour (AAAA-MM-JJ) : "
                )

                gestion.enregistrer_retour(identifiant, date)

            elif choix == "10":
                menu_maintenance()

            elif choix == "11":
                menu_rechercher_vehicule()

            elif choix == "12":
                gestion.afficher_statistiques()

            elif choix == "13":
                gestion.afficher_historique()

            else:
                print("Choix invalide.")

        except (ValueError, OSError, RuntimeError) as erreur:

            print("Erreur :", erreur)


# ==================================================
# POINT DE DEPART DU PROGRAMME
# ==================================================

# Cette condition vérifie si main.py est exécuté directement.
# Si c'est le cas, on démarre le programme avec main().

if __name__ == "__main__":
    main()
