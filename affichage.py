# affichage.py
# Couleurs de texte
from email.mime import message

import tache


ROUGE    = "\033[91m"
VERT     = "\033[92m"
JAUNE    = "\033[93m"
BLEU     = "\033[94m"
MAGENTA  = "\033[95m"
CYAN     = "\033[96m"
BLANC    = "\033[97m"
RESET    = "\033[0m"   
# Revenir a la couleur par defaut
# Styles
GRAS     = "\033[1m"
SOULIGNE = "\033[4m"
# Exemple d'utilisation
def afficher_succes(message):
print(f"{VERT}{GRAS}[OK]{RESET} {message}")
def afficher_erreur(message):
print(f"{ROUGE}{GRAS}[ERREUR]{RESET} {message}")
def afficher_info(message):
print(f"{CYAN}[INFO]{RESET} {message}")
def afficher_alerte(message):
print(f"{JAUNE}{GRAS}[!]{RESET} {message}")
def afficher_menu_principal(nom_utilisateur):
""" Affiche le menu principal apres connexion.
PISTE : utilisez les separateurs, les couleurs et l'alignement
pour rendre le menu lisible.
"""
print("\n" + "=" * 50)
print(f"{BLEU}{GRAS}  TASKFLOW — Bienvenue, {nom_utilisateur}{RESET}")
print("=" * 50)
print(f"  {GRAS}1.{RESET} Voir toutes mes taches")
print(f"  {GRAS}2.{RESET} Ajouter une nouvelle tache")
print(f"  {GRAS}3.{RESET} Modifier une tache")
print(f"  {GRAS}4.{RESET} Changer le statut d'une tache")
print(f"  {GRAS}5.{RESET} Supprimer une tache")
print(f"  {GRAS}6.{RESET} Gerer mes categories")
print(f"  {GRAS}7.{RESET} Gerer mes etiquettes")
print(f"  {GRAS}8.{RESET} Voir l'historique d'une tache")
print(f"  {GRAS}9.{RESET} Rechercher des taches")
print(f"  {GRAS}0.{RESET} {ROUGE}Se deconnecter{RESET}")
print("=" * 50)
def afficher_tache(tache):
"""
Affiche les details d'une tache de facon lisible.
tache est un dictionnaire retourne par la base de donnees.
PISTE : utilisez les couleurs selon la priorite et le statut.
"""
# Association priorite → couleur
couleurs_priorite = { "basse"
   : BLEU,
"normale" : BLANC,
"haute"
   : JAUNE,
"urgente" : ROUGE
}
# Association statut → symbole
symboles_statut = {
"a_faire"  : "[ ]",
"en_cours" : "[~]",
"terminee" : "[X]",
"annulee"  : "[-]"
}
couleur = couleurs_priorite.get(tache["priorite"], BLANC)
symbole = symboles_statut.get(tache["statut"], "[ ]")
print(f"\n  {symbole} {couleur}{GRAS}{tache['titre']}{RESET}")
print(f"     Priorite  : {couleur}{tache['priorite']}{RESET}")
print(f"     Statut    : {tache['statut']}")
print(f"     Echeance  : {tache.get('date_echeance', 'Non definie')}")
print(f"     Categorie : {tache.get('nom_categorie', 'Aucune')}")
if tache.get("description"):
print(f"     Detail    : {tache['description']}")
print()
def vider_ecran():
"""Efface le terminal pour un affichage propre."""
import os
os.system("cls" if os.name == "nt" else "clear")
