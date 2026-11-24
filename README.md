# Gestionnaire de Location de Véhicules

**Projet 1**  
**Auteur : Carl Stevens Leon**

---

## Présentation du projet

Le **Gestionnaire de Location de Véhicules** est un projet développé en Python. Il repose sur l'approche de la **programmation orientée objet (POO)** et utilise un fichier JSON pour conserver les données.

Ce document présente l'organisation générale du projet, ses principaux éléments et les concepts de programmation utilisés.

## Informations générales

| Élément | Description |
|---|---|
| Langage | Python |
| Approche | Programmation orientée objet (POO) |
| Persistance des données | Fichier JSON |
| Fichier de données | `location_data.json` |

## Organisation des fichiers

| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée du programme et interface console. Affiche le menu, récupère les choix et les informations saisies par l'utilisateur, puis appelle les méthodes du gestionnaire. |
| `Prototype.py` | Contient les classes et les objets du projet, notamment `Vehicule`, `Voiture`, `Moto`, `Client`, `Reservation`, `Maintenance` et `Historique`. |
| `Gestion_location.py` | Regroupe la logique de gestion et coordonne les opérations du système. |
| `location_data.json` | Fichier utilisé pour stocker les données afin de les retrouver lors d'une prochaine exécution. |

## Concepts de programmation utilisés

### 1. Classes et objets

Une classe décrit un type d'objet. Un objet est un exemplaire créé à partir de cette classe.

Dans ce projet, les classes représentent les différents éléments nécessaires à la gestion de la location : véhicules, clients, réservations, maintenances et historique.

### 2. Encapsulation

L'encapsulation consiste à protéger certaines données internes d'un objet. Par exemple, un attribut comme `_tarif_journalier` est destiné à être manipulé de manière contrôlée, notamment à l'aide de propriétés.

### 3. Héritage

L'héritage permet à une classe de reprendre les caractéristiques d'une autre classe.

Dans le projet :
- `Voiture` est un type de `Vehicule`.
- `Moto` est un type de `Vehicule`.

Les deux classes spécialisées peuvent ainsi partager les caractéristiques communes définies dans `Vehicule`.

### 4. Association

Une réservation est associée à un client. Cette relation permet de relier les informations d'une réservation au client concerné.

### 5. Composition et gestion des collections

Le gestionnaire regroupe et coordonne les objets nécessaires au fonctionnement du programme, ainsi que les opérations qui leur sont associées.

### 6. Persistance des données

Le format JSON permet de sauvegarder les données du programme dans le fichier `location_data.json`, puis de les retrouver lors d'une prochaine exécution.

## Fonctionnement général

Le fichier `main.py` constitue le point d'entrée du programme :

1. Le programme affiche le menu principal.
2. L'utilisateur choisit une opération.
3. Le programme récupère les informations nécessaires.
4. `main.py` fait appel aux méthodes du gestionnaire.
5. Le gestionnaire coordonne les opérations sur les objets concernés.
6. Les données sont sauvegardées dans le fichier JSON afin de pouvoir être réutilisées.

## Éléments représentés dans le modèle

- **Vehicule** : représente un véhicule.
- **Voiture** : représente un véhicule de type voiture.
- **Moto** : représente un véhicule de type moto.
- **Client** : représente un client.
- **Reservation** : représente une réservation associée à un client.
- **Maintenance** : représente les informations liées à la maintenance.
- **Historique** : regroupe les informations historiques du système.

## Lancement du projet

Le programme est prévu pour être lancé à partir de son point d'entrée `main.py`.

Dans un terminal, placez-vous dans le dossier du projet, puis exécutez :

```bash
python main.py
```

Selon votre installation, la commande peut être :

```bash
python3 main.py
```

**Remarque :** les fichiers `main.py`, `Prototype.py`, `Gestion_location.py` et `location_data.json` doivent être placés conformément à l'organisation du projet.

## Auteur

Projet 1 préparé par :

**Carl Stevens Leon**

---

*Gestionnaire de Location de Véhicules — Documentation du projet*
