"""
Ce module est responsable de la gestion des utilisateurs dans l'application IFT-1004 DuProprio,
incluant l'enregistrement de nouveaux utilisateurs et la connexion des utilisateurs existants.
Il interagit avec le fichier des utilisateurs pour enregistrer et vérifier les informations des utilisateurs,
tels que les noms d'utilisateurs et les mots de passe (sous forme hachée).

Fonctions:
- `creer_compte()`: Crée un nouveau compte utilisateur.
- `se_connecter()`: Connecte un utilisateur existant en vérifiant son nom d'utilisateur et son mot de passe.
- `se_deconnecter()`: Déconnecte l'utilisateur actuel.
- `utilisateur_est_connecte()`: Vérifie si un utilisateur est connecté.
- `recuperer_utilisateur_courant()`: Récupère l'utilisateur actuellement connecté.
- `definir_utilisateur_courant(nom_utilisateur)`: Définit l'utilisateur actuellement connecté.
- `vider_session()`: Efface les informations de session de l'utilisateur actuellement connecté.

Dépendances:
- `secrets`: Pour comparer les hachages (https://docs.python.org/3/library/secrets.html#secrets.compare_digest).
- `gestionnaire_donnees`: Pour lire et écrire dans le fichier des utilisateurs.
- `utilitaires`: Pour hacher les mots de passe.
- `configuration`: Pour accéder au chemin du fichier de session.
"""

import secrets
from gestionnaire_donnees import charger_utilisateurs, sauvegarder_utilisateurs
from utilitaires import hacher_mot_de_passe
from configuration import FICHIER_SESSION


def recuperer_utilisateur_courant():
    """Récupère l'utilisateur actuellement connecté."""
    try:
        with open(FICHIER_SESSION, "r") as f:
            if f.read().strip() == "":
                return None
            else:
                return f.read().strip()
    except FileNotFoundError:
        return None

def definir_utilisateur_courant(nom_utilisateur):
    """Définit l'utilisateur actuellement connecté."""
    with open(FICHIER_SESSION, "w") as f:
        f.write(nom_utilisateur)


def vider_session():
    """Efface les informations de session de l'utilisateur actuellement connecté."""
    with open(FICHIER_SESSION, "w") as f:
        f.write("")


def creer_compte():
    """Crée un nouveau compte utilisateur."""
    utilisateurs = charger_utilisateurs()
    nom_utilisateur = input("Nom d'utilisateur: ").strip()
    if nom_utilisateur in utilisateurs:
        print("Ce nom d'utilisateur est déjà pris.")
        return

    mot_de_passe = input("Mot de passe: ").strip()
    utilisateurs[nom_utilisateur] = hacher_mot_de_passe(mot_de_passe)
    sauvegarder_utilisateurs(utilisateurs)
    print("Compte créé avec succès.")


def se_connecter():
    """Connecte un utilisateur existant."""
    utilisateurs = charger_utilisateurs()
    nom_utilisateur = input("Nom d'utilisateur: ").strip()
    mot_de_passe = input("Mot de passe: ").strip()
    mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe)

    if utilisateurs.get(nom_utilisateur) == mot_de_passe_hache:
        definir_utilisateur_courant(nom_utilisateur)
        print("Connexion réussie.")
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")


def se_deconnecter():
    """Déconnecte l'utilisateur actuel."""
    vider_session()
    print("Déconnexion réussie.")
    


def utilisateur_est_connecte():
    """Vérifie si un utilisateur est connecté."""
    return recuperer_utilisateur_courant() is not None
