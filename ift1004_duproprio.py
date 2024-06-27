"""
Point d'entrée principal pour l'application IFT-1004 DuProprio.

Ce module coordonne le déroulement général de l'application, de l'affichage de la bannière de bienvenue,
à l'affichage des menus et la gestion de l'interaction avec l'utilisateur.

Les utilisateurs peuvent créer un compte, se connecter, ajouter des propriétés, consulter les propriétés existantes,
filtrer les propriétés, ou se déconnecter. Les interactions sont gérées à travers une boucle principale
qui sollicite l'action de l'utilisateur et appelle les fonctions appropriées en réponse.

Fonctions:
- main(): Lance l'application, gérant le flux principal et les interactions utilisateur.

Ce module utilise des fonctions définies dans d'autres modules comme `gestionnaire_proprietes`,
`gestionnaire_utilisateurs`, et `utilitaires` pour accomplir ses tâches.
"""

from gestionnaire_proprietes import (
    lister_proprietes,
    filtrer_proprietes,
    ajouter_propriete,
)
from gestionnaire_utilisateurs import (
    creer_compte,
    se_connecter,
    se_deconnecter,
    utilisateur_est_connecte,
)
from utilitaires import afficher_banniere


def main():
    """Fonction principale qui gère l'interaction avec l'utilisateur.

    Cette fonction affiche une bannière de bienvenue et propose un menu d'options
    permettant de lister les propriétés, filtrer les propriétés, créer un compte,
    se connecter, se déconnecter et ajouter une propriété si un utilisateur est connecté.

    L'utilisateur peut choisir une option en entrant le numéro correspondant, et la boucle
    continue jusqu'à ce que l'utilisateur choisisse de quitter.
    """
    afficher_banniere("Bienvenue sur IFT-1004 DuProprio !")

    continuer = True
    while continuer:
        print("\nOptions:")
        print("1. Lister les propriétés")
        print("2. Filtrer les propriétés")
        if utilisateur_est_connecte():
            print("3. Ajouter une propriété")
            print("4. Déconnexion")
        else:
            print("3. Créer un compte")
            print("4. Connexion")
        print("5. Quitter")

        choix = input("Choisissez une option: ")

        if choix == "1":
            lister_proprietes()
        elif choix == "2":
            filtrer_proprietes()
        elif choix == "3" and utilisateur_est_connecte():
            ajouter_propriete()
        elif choix == "3":
            creer_compte()
        elif choix == "4" and utilisateur_est_connecte():
            se_deconnecter()
        elif choix == "4":
            se_connecter()
        elif choix == "5":
            print(
                "IFT-1004 DuProprio: Trouvez votre chez-vous, sans les agents embêtants !"
            )
            continuer = False
        else:
            print("Option invalide.")


if __name__ == "__main__":
    main()
