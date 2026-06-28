# historique.py
from mysql.connector import Error
from connexion import obtenir_connexion, fermer_connexion
import affichage


# ---------- F20 - Consulter l'historique d'une tache ----------

def obtenir_historique_tache(id_tache):
    """
    Retourne la liste des changements de statut d'une tache,
    tries du plus recent au plus ancien.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT * FROM HISTORIQUE
            WHERE id_tache = %s
            ORDER BY date_changement DESC
        """
        cursor.execute(sql, (id_tache,))
        return cursor.fetchall()
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def afficher_historique(historique, titre_tache):
    """Affiche les entrees d'historique de facon lisible."""
    print(f"\n--- Historique de la tache : {titre_tache} ---")
    if not historique:
        affichage.afficher_info("Aucun changement de statut enregistre pour cette tache.")
        return

    for entree in historique:
        ancien = entree["ancien_statut"] or "creation"
        print(f"\n  {entree['date_changement']}")
        print(f"  {ancien} -> {entree['nouveau_statut']}")
        if entree.get("commentaire"):
            print(f"  Commentaire : {entree['commentaire']}")


def menu_voir_historique(id_user):
    from tache import obtenir_tache

    print("\n--- Voir l'historique d'une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    historique = obtenir_historique_tache(int(id_tache))
    if historique is not None:
        afficher_historique(historique, tache["titre"])


# ---------- F21 - Statistiques personnelles ----------

def calculer_statistiques(id_user):
    """
    Calcule les statistiques personnelles d'un utilisateur :
    total, repartition par statut, repartition par priorite, taux de completion.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)

        # Total
        cursor.execute("SELECT COUNT(*) AS total FROM TACHE WHERE id_user = %s", (id_user,))
        total = cursor.fetchone()["total"]

        # Par statut
        cursor.execute("""
            SELECT statut, COUNT(*) AS nb FROM TACHE
            WHERE id_user = %s GROUP BY statut
        """, (id_user,))
        lignes_statut = cursor.fetchall()
        par_statut = {"a_faire": 0, "en_cours": 0, "terminee": 0, "annulee": 0}
        for ligne in lignes_statut:
            par_statut[ligne["statut"]] = ligne["nb"]

        # Par priorite
        cursor.execute("""
            SELECT priorite, COUNT(*) AS nb FROM TACHE
            WHERE id_user = %s GROUP BY priorite
        """, (id_user,))
        lignes_priorite = cursor.fetchall()
        par_priorite = {"basse": 0, "normale": 0, "haute": 0, "urgente": 0}
        for ligne in lignes_priorite:
            par_priorite[ligne["priorite"]] = ligne["nb"]

        # Taux de completion
        taux_completion = (par_statut["terminee"] / total * 100) if total else 0.0

        return {
            "total": total,
            "par_statut": par_statut,
            "par_priorite": par_priorite,
            "taux_completion": taux_completion
        }
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_statistiques(id_user):
    stats = calculer_statistiques(id_user)
    if stats is not None:
        if stats["total"] == 0:
            affichage.afficher_info("Vous n'avez encore aucune tache.")
            return
        affichage.afficher_statistiques(stats)