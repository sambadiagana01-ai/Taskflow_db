# affichage.py
import os

# Couleurs de texte
ROUGE = "\033[91m"
VERT = "\033[92m"
JAUNE = "\033[93m"
BLEU = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLANC = "\033[97m"
RESET = "\033[0m"  # Revenir a la couleur par defaut

# Styles
GRAS = "\033[1m"
SOULIGNE = "\033[4m"


# ---------- Messages generaux ----------

def afficher_succes(message):
    print(f"{VERT}{GRAS}[OK]{RESET} {message}")


def afficher_erreur(message):
    print(f"{ROUGE}{GRAS}[ERREUR]{RESET} {message}")


def afficher_info(message):
    print(f"{CYAN}[INFO]{RESET} {message}")


def afficher_alerte(message):
    print(f"{JAUNE}{GRAS}[!]{RESET} {message}")


def vider_ecran():
    """Efface le terminal pour un affichage propre."""
    os.system("cls" if os.name == "nt" else "clear")


# ---------- Menus ----------

def afficher_menu_accueil():
    """Menu avant connexion : inscription ou connexion."""
    print("\n" + "=" * 50)
    print(f"{MAGENTA}{GRAS} TASKFLOW — Gestionnaire de taches{RESET}")
    print("=" * 50)
    print(f" {GRAS}1.{RESET} Se connecter")
    print(f" {GRAS}2.{RESET} S'inscrire")
    print(f" {GRAS}0.{RESET} {ROUGE}Quitter{RESET}")
    print("=" * 50)


def afficher_menu_principal(nom_utilisateur):
    print("\n" + "=" * 50)
    print(f"{BLEU}{GRAS} TASKFLOW — Bienvenue, {nom_utilisateur}{RESET}")
    print("=" * 50)
    print(f" {GRAS}1.{RESET} Voir toutes mes taches")
    print(f" {GRAS}2.{RESET} Ajouter une nouvelle tache")
    print(f" {GRAS}3.{RESET} Modifier une tache")
    print(f" {GRAS}4.{RESET} Changer le statut d'une tache")
    print(f" {GRAS}5.{RESET} Supprimer une tache")
    print(f" {GRAS}6.{RESET} Gerer mes categories")
    print(f" {GRAS}7.{RESET} Gerer mes etiquettes")
    print(f" {GRAS}8.{RESET} Voir l'historique d'une tache")
    print(f" {GRAS}9.{RESET} Rechercher / filtrer des taches")
    print(f" {GRAS}10.{RESET} Statistiques personnelles")
    print(f" {GRAS}0.{RESET} {ROUGE}Se deconnecter{RESET}")
    print("=" * 50)


def afficher_menu_filtres():
    print("\n" + "-" * 40)
    print(f"{CYAN}{GRAS} Recherche et filtrage{RESET}")
    print("-" * 40)
    print(f" {GRAS}1.{RESET} Filtrer par statut")
    print(f" {GRAS}2.{RESET} Filtrer par priorite")
    print(f" {GRAS}3.{RESET} Filtrer par categorie")
    print(f" {GRAS}4.{RESET} Recherche par mot-cle")
    print(f" {GRAS}5.{RESET} Taches en retard")
    print(f" {GRAS}6.{RESET} Taches du jour")
    print(f" {GRAS}0.{RESET} Retour")
    print("-" * 40)


def afficher_menu_categories():
    print("\n" + "-" * 40)
    print(f"{CYAN}{GRAS} Gestion des categories{RESET}")
    print("-" * 40)
    print(f" {GRAS}1.{RESET} Creer une categorie")
    print(f" {GRAS}2.{RESET} Lister mes categories")
    print(f" {GRAS}3.{RESET} Supprimer une categorie")
    print(f" {GRAS}0.{RESET} Retour")
    print("-" * 40)


def afficher_menu_etiquettes():
    print("\n" + "-" * 40)
    print(f"{CYAN}{GRAS} Gestion des etiquettes{RESET}")
    print("-" * 40)
    print(f" {GRAS}1.{RESET} Ajouter une etiquette a une tache")
    print(f" {GRAS}2.{RESET} Retirer une etiquette d'une tache")
    print(f" {GRAS}0.{RESET} Retour")
    print("-" * 40)


# ---------- Affichage des taches ----------

COULEURS_PRIORITE = {
    "basse": BLEU,
    "normale": BLANC,
    "haute": JAUNE,
    "urgente": ROUGE
}

SYMBOLES_STATUT = {
    "a_faire": "[ ]",
    "en_cours": "[~]",
    "terminee": "[X]",
    "annulee": "[-]"
}


def afficher_tache(tache):
    """
    Affiche les details d'une tache de facon lisible.
    tache est un dictionnaire retourne par la base de donnees.
    """
    couleur = COULEURS_PRIORITE.get(tache["priorite"], BLANC)
    symbole = SYMBOLES_STATUT.get(tache["statut"], "[ ]")

    print(f"\n {symbole} {couleur}{GRAS}#{tache['id_tache']} - {tache['titre']}{RESET}")
    print(f"    Priorite  : {couleur}{tache['priorite']}{RESET}")
    print(f"    Statut    : {tache['statut']}")
    print(f"    Echeance  : {tache.get('date_echeance') or 'Non definie'}")
    print(f"    Categorie : {tache.get('nom_categorie') or 'Aucune'}")
    if tache.get("description"):
        print(f"    Detail    : {tache['description']}")


def afficher_liste_taches(taches):
    """
    Affiche une liste de taches sous forme de tableau resume.
    taches est une liste de dictionnaires.
    """
    if not taches:
        afficher_info("Aucune tache a afficher.")
        return

    print("\n" + "-" * 70)
    print(f"{GRAS}{'ID':<4}{'Titre':<25}{'Statut':<12}{'Priorite':<10}{'Echeance':<12}{RESET}")
    print("-" * 70)
    for t in taches:
        couleur = COULEURS_PRIORITE.get(t["priorite"], BLANC)
        symbole = SYMBOLES_STATUT.get(t["statut"], "[ ]")
        echeance = t.get("date_echeance") or "-"
        print(f"{symbole} {couleur}{t['id_tache']:<2}{RESET} "
              f"{t['titre'][:23]:<25}{t['statut']:<12}"
              f"{couleur}{t['priorite']:<10}{RESET}{str(echeance):<12}")
    print("-" * 70)
    print(f"Total : {len(taches)} tache(s)\n")


def afficher_tableau_categories(categories):
    """
    categories est une liste de dicts avec au moins nom_categorie, couleur,
    et idealement nb_taches (nombre de taches associees).
    """
    if not categories:
        afficher_info("Aucune categorie pour le moment.")
        return

    print("\n" + "-" * 50)
    print(f"{GRAS}{'ID':<4}{'Nom':<20}{'Couleur':<12}{'Nb taches':<10}{RESET}")
    print("-" * 50)
    for c in categories:
        nb = c.get("nb_taches", "-")
        print(f"{c['id_categorie']:<4}{c['nom_categorie']:<20}{c['couleur']:<12}{nb}")
    print("-" * 50)


def afficher_etiquettes(etiquettes):
    if not etiquettes:
        afficher_info("Aucune etiquette.")
        return
    noms = ", ".join(f"#{e['nom_etiquette']}" for e in etiquettes)
    print(f"    Etiquettes : {CYAN}{noms}{RESET}")


def afficher_statistiques(stats):
    """
    stats est un dict avec les cles : total, par_statut (dict), par_priorite (dict),
    taux_completion (float)
    """
    print("\n" + "=" * 40)
    print(f"{MAGENTA}{GRAS} Statistiques personnelles{RESET}")
    print("=" * 40)
    print(f" Total de taches : {GRAS}{stats['total']}{RESET}")
    print("\n Par statut :")
    for statut, nb in stats["par_statut"].items():
        pourcentage = (nb / stats["total"] * 100) if stats["total"] else 0
        print(f"   {statut:<12}: {nb:<3} ({pourcentage:.1f}%)")
    print("\n Par priorite :")
    for priorite, nb in stats["par_priorite"].items():
        couleur = COULEURS_PRIORITE.get(priorite, BLANC)
        pourcentage = (nb / stats["total"] * 100) if stats["total"] else 0
        print(f"   {couleur}{priorite:<12}{RESET}: {nb:<3} ({pourcentage:.1f}%)")
    print(f"\n {VERT}{GRAS}Taux de completion : {stats['taux_completion']:.1f}%{RESET}")
    print("=" * 40)