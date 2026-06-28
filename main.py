# main.py
import affichage
from utilisateur import menu_inscription, menu_connexion, deconnecter_utilisateur

from tache import (
    menu_ajouter_tache, menu_lister_taches, menu_detail_tache,
    menu_modifier_tache, menu_changer_statut, menu_supprimer_tache,
    menu_filtrer_par_statut, menu_filtrer_par_priorite, menu_filtrer_par_categorie,
    menu_rechercher, menu_taches_en_retard, menu_taches_du_jour
)
from categorie import menu_creer_categorie, menu_lister_categories, menu_supprimer_categorie
from etiquette import menu_ajouter_etiquette, menu_retirer_etiquette
from historique import menu_voir_historique, menu_statistiques


def menu_accueil():
    """
    Boucle d'accueil : inscription / connexion / quitter.
    Retourne le dict utilisateur connecte, ou None si l'utilisateur quitte.
    """
    while True:
        affichage.afficher_menu_accueil()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            utilisateur = menu_connexion()
            if utilisateur:
                return utilisateur

        elif choix == "2":
            utilisateur = menu_inscription()
            if utilisateur:
                return utilisateur

        elif choix == "0":
            return None

        else:
            affichage.afficher_erreur("Choix invalide.")


def sous_menu_filtres(id_user):
    while True:
        affichage.afficher_menu_filtres()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_filtrer_par_statut(id_user)
        elif choix == "2":
            menu_filtrer_par_priorite(id_user)
        elif choix == "3":
            menu_filtrer_par_categorie(id_user)
        elif choix == "4":
            menu_rechercher(id_user)
        elif choix == "5":
            menu_taches_en_retard(id_user)
        elif choix == "6":
            menu_taches_du_jour(id_user)
        elif choix == "0":
            return
        else:
            affichage.afficher_erreur("Choix invalide.")


def sous_menu_categories(id_user):
    while True:
        affichage.afficher_menu_categories()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_creer_categorie(id_user)
        elif choix == "2":
            menu_lister_categories(id_user)
        elif choix == "3":
            menu_supprimer_categorie(id_user)
        elif choix == "0":
            return
        else:
            affichage.afficher_erreur("Choix invalide.")


def sous_menu_etiquettes(id_user):
    while True:
        affichage.afficher_menu_etiquettes()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_ajouter_etiquette(id_user)
        elif choix == "2":
            menu_retirer_etiquette(id_user)
        elif choix == "0":
            return
        else:
            affichage.afficher_erreur("Choix invalide.")


def menu_principal(utilisateur):
    """
    Boucle du menu principal apres connexion.
    Retourne quand l'utilisateur se deconnecte (choix 0).
    """
    id_user = utilisateur["id_user"]

    while True:
        affichage.afficher_menu_principal(utilisateur["nom_utilisateur"])
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_lister_taches(id_user)
        elif choix == "2":
            menu_ajouter_tache(id_user)
        elif choix == "3":
            menu_modifier_tache(id_user)
        elif choix == "4":
            menu_changer_statut(id_user)
        elif choix == "5":
            menu_supprimer_tache(id_user)
        elif choix == "6":
            sous_menu_categories(id_user)
        elif choix == "7":
            sous_menu_etiquettes(id_user)
        elif choix == "8":
            menu_voir_historique(id_user)
        elif choix == "9":
            sous_menu_filtres(id_user)
        elif choix == "10":
            menu_statistiques(id_user)
        elif choix == "0":
            deconnecter_utilisateur()
            return
        else:
            affichage.afficher_erreur("Choix invalide.")

        input("\nAppuyez sur Entree pour continuer...")


def main():
    """Point d'entree de l'application."""
    affichage.afficher_info("Demarrage de TaskFlow...")

    while True:
        utilisateur_connecte = menu_accueil()

        if utilisateur_connecte is None:
            affichage.afficher_info("A bientot !")
            break

        menu_principal(utilisateur_connecte)
        # Apres deconnexion, on retourne au menu d'accueil (boucle while)


if __name__ == "__main__":
    main()