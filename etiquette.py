# etiquette.py
from mysql.connector import Error
from connexion import obtenir_connexion, fermer_connexion
import affichage


def lister_etiquettes(id_user):
    """Retourne toutes les etiquettes de l'utilisateur."""
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM ETIQUETTE WHERE id_user = %s ORDER BY nom_etiquette"
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


def creer_etiquette(id_user, nom_etiquette):
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = "INSERT INTO ETIQUETTE (nom_etiquette, id_user) VALUES (%s, %s)"
        cursor.execute(sql, (nom_etiquette, id_user))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de la creation de l'etiquette : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


# ---------- F18 - Ajouter une etiquette a une tache ----------

def associer_etiquette_tache(id_tache, id_etiquette):
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        sql = "INSERT INTO TACHE_ETIQUETTE (id_tache, id_etiquette) VALUES (%s, %s)"
        cursor.execute(sql, (id_tache, id_etiquette))
        conn.commit()
        return True
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de l'association : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_ajouter_etiquette(id_user):
    from tache import obtenir_tache

    print("\n--- Ajouter une etiquette a une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    etiquettes = lister_etiquettes(id_user)
    if etiquettes:
        print("\nVos etiquettes existantes :")
        for e in etiquettes:
            print(f"  {e['id_etiquette']}. #{e['nom_etiquette']}")
        print("  0. Creer une nouvelle etiquette")
    else:
        affichage.afficher_info("Vous n'avez aucune etiquette. Creons-en une.")

    choix = input("Numero de l'etiquette (ou 0 pour en creer une) : ").strip()

    if choix == "0" or not etiquettes:
        nom = input("Nom de la nouvelle etiquette : ").strip()
        if not nom:
            affichage.afficher_erreur("Le nom ne peut pas etre vide.")
            return
        id_etiquette = creer_etiquette(id_user, nom)
        if not id_etiquette:
            affichage.afficher_erreur("La creation a echoue.")
            return
    elif choix.isdigit():
        id_etiquette = int(choix)
    else:
        affichage.afficher_erreur("Choix invalide.")
        return

    succes = associer_etiquette_tache(int(id_tache), id_etiquette)
    if succes:
        affichage.afficher_succes("Etiquette ajoutee a la tache.")
    else:
        affichage.afficher_erreur("L'ajout a echoue (peut-etre deja associee).")


# ---------- F19 - Retirer une etiquette d'une tache ----------

def retirer_etiquette_tache(id_tache, id_etiquette):
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        sql = "DELETE FROM TACHE_ETIQUETTE WHERE id_tache = %s AND id_etiquette = %s"
        cursor.execute(sql, (id_tache, id_etiquette))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors du retrait : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_retirer_etiquette(id_user):
    from tache import obtenir_tache, obtenir_etiquettes_tache

    print("\n--- Retirer une etiquette d'une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    etiquettes = obtenir_etiquettes_tache(int(id_tache))
    if not etiquettes:
        affichage.afficher_info("Cette tache n'a aucune etiquette.")
        return

    print("\nEtiquettes de cette tache :")
    for e in etiquettes:
        print(f"  {e['id_etiquette']}. #{e['nom_etiquette']}")

    choix = input("Numero de l'etiquette a retirer : ").strip()
    if not choix.isdigit():
        affichage.afficher_erreur("Choix invalide.")
        return

    succes = retirer_etiquette_tache(int(id_tache), int(choix))
    if succes:
        affichage.afficher_succes("Etiquette retiree.")
    else:
        affichage.afficher_erreur("Le retrait a echoue.")