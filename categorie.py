# categorie.py
from mysql.connector import Error
from connexion import obtenir_connexion, fermer_connexion
import affichage

COULEURS_DISPONIBLES = ["rouge", "vert", "bleu", "jaune", "magenta", "cyan", "blanc"]


# ---------- F15 - Creer une categorie ----------

def inserer_categorie(id_user, nom_categorie, couleur):
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = "INSERT INTO CATEGORIE (nom_categorie, couleur, id_user) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nom_categorie, couleur, id_user))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de la creation de la categorie : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_creer_categorie(id_user):
    print("\n--- Creer une categorie ---")
    nom_categorie = input("Nom de la categorie : ").strip()
    if not nom_categorie:
        affichage.afficher_erreur("Le nom est obligatoire.")
        return

    print(f"Couleurs disponibles : {', '.join(COULEURS_DISPONIBLES)}")
    couleur = input("Couleur (par defaut 'blanc') : ").strip().lower()
    if couleur not in COULEURS_DISPONIBLES:
        couleur = "blanc"

    id_categorie = inserer_categorie(id_user, nom_categorie, couleur)
    if id_categorie:
        affichage.afficher_succes(f"Categorie '{nom_categorie}' creee (id {id_categorie}).")
    else:
        affichage.afficher_erreur("La creation a echoue.")


# ---------- F16 - Lister les categories ----------

def lister_categories(id_user):
    """
    Retourne la liste des categories de l'utilisateur,
    SANS le nombre de taches (utilise par tache.py / etiquette.py pour les menus).
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM CATEGORIE WHERE id_user = %s ORDER BY nom_categorie"
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def lister_categories_avec_compte(id_user):
    """
    Retourne les categories avec le nombre de taches associees,
    pour l'affichage detaille (F16).
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT c.*, COUNT(t.id_tache) AS nb_taches
            FROM CATEGORIE c
            LEFT JOIN TACHE t ON c.id_categorie = t.id_categorie
            WHERE c.id_user = %s
            GROUP BY c.id_categorie
            ORDER BY c.nom_categorie
        """
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_lister_categories(id_user):
    categories = lister_categories_avec_compte(id_user)
    if categories is not None:
        affichage.afficher_tableau_categories(categories)


# ---------- F17 - Supprimer une categorie ----------

def supprimer_categorie(id_categorie, id_user):
    """
    Supprime une categorie. Grace a ON DELETE SET NULL sur TACHE.id_categorie,
    les taches de cette categorie passent automatiquement a NULL.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        sql = "DELETE FROM CATEGORIE WHERE id_categorie = %s AND id_user = %s"
        cursor.execute(sql, (id_categorie, id_user))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de la suppression : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_supprimer_categorie(id_user):
    categories = lister_categories(id_user)
    if not categories:
        affichage.afficher_info("Vous n'avez aucune categorie.")
        return

    affichage.afficher_tableau_categories(categories)
    choix = input("Numero de la categorie a supprimer : ").strip()
    if not choix.isdigit():
        affichage.afficher_erreur("Choix invalide.")
        return

    categorie_choisie = next((c for c in categories if c["id_categorie"] == int(choix)), None)
    if not categorie_choisie:
        affichage.afficher_erreur("Categorie introuvable.")
        return

    confirmation = input(f"Supprimer '{categorie_choisie['nom_categorie']}' ? (o/n) : ").strip().lower()
    if confirmation == "o":
        succes = supprimer_categorie(int(choix), id_user)
        if succes:
            affichage.afficher_succes("Categorie supprimee. Ses taches passent en 'Aucune categorie'.")
        else:
            affichage.afficher_erreur("La suppression a echoue.")
    else:
        affichage.afficher_info("Suppression annulee.")