"""
Ce module est responsable de la gestion des propriétés dans l'application IFT-1004 DuProprio,
incluant l'ajout de nouvelles propriétés, la liste et le filtrage des propriétés disponibles.

Fonctions:
- `lister_proprietes()`: Liste toutes les propriétés disponibles.
- `filtrer_proprietes()`: Filtre les propriétés en fonction des critères de l'utilisateur.
- `ajouter_propriete()`: Ajoute une nouvelle propriété si l'utilisateur est connecté.

Dépendances:
- `gestionnaire_donnees`: Pour lire et écrire dans le fichier des propriétés.
- `gestionnaire_utilisateurs`: Pour vérifier si un utilisateur est connecté.
- `utilitaires`: Pour des fonctions auxiliaires comme l'affichage de tableaux formatés,
et le formatage de montants en dollars.
"""

from gestionnaire_donnees import charger_proprietes, sauvegarder_propriete
from gestionnaire_utilisateurs import recuperer_utilisateur_courant, utilisateur_est_connecte
from utilitaires import afficher_tableau, formater_argent, afficher_banniere


TYPES_DE_PROPRIETE = ["Maison", "Appartement", "Condo", "Studio"]
VILLES = ["Québec", "Montréal", "Toronto", "Ottawa"]


def lister_proprietes():
    """Liste toutes les propriétés disponibles."""
    proprietes = charger_proprietes()
    
    if not proprietes:
        print("Aucune propriété disponible.")
        return
    
    # Formater les propriétés pour l'affichage
    proprietes_formatees = [
        [
            propriete["ville"],
            propriete["type"],
            propriete["chambres"],
            propriete["salles de bains"],
            formater_argent(propriete["prix"])
        ]
        for propriete in proprietes
    ]
    
    # Afficher le tableau des propriétés
    en_tetes = ["Ville", "Type", "Chambres", "Salles de Bains", "Prix"]
    afficher_tableau(proprietes_formatees, en_tetes)


def filtrer_proprietes():
    """Filtre les propriétés en fonction de critères donnés par l'utilisateur."""
    proprietes = charger_proprietes()
    critere_ville = input("Ville (laisser vide pour ignorer): ").strip()
    critere_prix_min = input("Prix minimum (laisser vide pour ignorer): ").strip()
    critere_prix_max = input("Prix maximum (laisser vide pour ignorer): ").strip()
    critere_chambres = input("Nombre de chambres minimum (laisser vide pour ignorer): ").strip()

    if critere_prix_min:
        critere_prix_min = float(critere_prix_min)
    if critere_prix_max:
        critere_prix_max = float(critere_prix_max)
    if critere_chambres:
        critere_chambres = int(critere_chambres)

    proprietes_filtrees = []
    for propriete in proprietes:
        if critere_ville and propriete["ville"] != critere_ville:
            continue
        if critere_prix_min and propriete["prix"] < critere_prix_min:
            continue
        if critere_prix_max and propriete["prix"] > critere_prix_max:
            continue
        if critere_chambres and propriete["chambres"] < critere_chambres:
            continue
        proprietes_filtrees.append(propriete)

    for propriete in proprietes_filtrees:
        print(propriete)

def ajouter_propriete():
    """Ajoute une nouvelle propriété."""
    utilisateur = recuperer_utilisateur_courant()
    if not utilisateur:
        print("Vous devez être connecté pour ajouter une propriété.")
        return

    prix = float(input("Prix: "))
    ville = input("Ville: ").strip()
    type_propriete = input("Type (Maison, Condo, etc.): ").strip()
    chambres = int(input("Nombre de chambres: "))
    salles_de_bain = int(input("Nombre de salles de bain: "))

    nouvelle_propriete = {
        "prix": prix,
        "ville": ville,
        "type": type_propriete,
        "chambres": chambres,
        "salles de bains": salles_de_bain
    }
    sauvegarder_propriete(nouvelle_propriete)
    print("Propriété ajoutée avec succès.")


def demander_plage_de_prix(optionnel=False):
    """Demande à l'utilisateur de saisir une plage de prix.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        tuple: (prix_minimum, prix_maximum)
    """
    while True:
        try:
            prix_minimum = input("Prix minimum: ")
            prix_maximum = input("Prix maximum: ")
            if optionnel and not prix_minimum and not prix_maximum:
                return None, None
            prix_minimum = int(prix_minimum) if prix_minimum else None
            prix_maximum = int(prix_maximum) if prix_maximum else None
            if (
                prix_minimum is not None
                and prix_maximum is not None
                and prix_minimum > prix_maximum
            ):
                raise ValueError(
                    "Le prix minimum doit être inférieur ou égal au prix maximum."
                )
            return prix_minimum, prix_maximum
        except ValueError as e:
            print(e)


def demander_ville(optionnel=False):
    """Demande à l'utilisateur de choisir une ville parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: La ville choisie.
    """
    print(f"Choisissez une ville parmi les suivantes: {', '.join(VILLES)}")
    while True:
        ville = input("Ville: ")
        if optionnel and not ville:
            return None
        if ville in VILLES:
            return ville
        print(f"Ville invalide. Choisissez parmi: {', '.join(VILLES)}")


def demander_type_de_propriete(optionnel=False):
    """Demande à l'utilisateur de choisir un type de propriété parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: Le type de propriété choisi.
    """
    print(
        f"Choisissez un type de propriété parmi les suivants: {', '.join(TYPES_DE_PROPRIETE)}"
    )
    while True:
        type_de_propriete = input("Type de propriété: ")
        if optionnel and not type_de_propriete:
            return None
        if type_de_propriete in TYPES_DE_PROPRIETE:
            return type_de_propriete
        print(
            f"Type de propriété invalide. Choisissez parmi: {', '.join(TYPES_DE_PROPRIETE)}"
        )


def demander_nombre(prompt, optionnel=False):
    """Demande à l'utilisateur de saisir un nombre.

    Args:
        prompt (str): Le message à afficher pour la saisie.
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        int: Le nombre saisi.
    """
    while True:
        nombre = input(f"{prompt}: ")
        if optionnel and not nombre:
            return None
        try:
            return int(nombre)
        except ValueError:
            print("Valeur invalide. Veuillez saisir un nombre.")
