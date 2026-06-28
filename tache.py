# tache.py
from mysql.connector import Error
from connexion import obtenir_connexion, fermer_connexion
import affichage


# ---------- F04 - Ajouter une tache ----------

def inserer_tache(id_user, titre, description, date_echeance, priorite, id_categorie):
    """
    Insere une nouvelle tache en base. Retourne l'id de la tache creee, ou None si echec.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor()
        sql = """INSERT INTO TACHE (titre, description, date_echeance, priorite, id_user, id_categorie)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valeurs = (titre, description or None, date_echeance or None, priorite, id_user, id_categorie)
        cursor.execute(sql, valeurs)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de l'ajout de la tache : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_ajouter_tache(id_user):
    """Gere le flux complet d'ajout d'une tache depuis le terminal."""
    print("\n--- Ajouter une nouvelle tache ---")
    titre = input("Titre (obligatoire) : ").strip()
    if not titre:
        affichage.afficher_erreur("Le titre est obligatoire.")
        return

    description = input("Description (optionnel) : ").strip()
    date_echeance = input("Date d'echeance (AAAA-MM-JJ, optionnel) : ").strip()

    print("Priorites disponibles : basse / normale / haute / urgente")
    priorite = input("Priorite (par defaut 'normale') : ").strip().lower()
    if priorite not in ("basse", "normale", "haute", "urgente"):
        priorite = "normale"

    # Choix de categorie : on importe ici pour eviter une dependance circulaire
    from categorie import lister_categories
    categories = lister_categories(id_user)
    id_categorie = None
    if categories:
        print("\nVos categories :")
        for c in categories:
            print(f"  {c['id_categorie']}. {c['nom_categorie']}")
        choix = input("Numero de categorie (vide = aucune) : ").strip()
        if choix.isdigit():
            id_categorie = int(choix)
    else:
        affichage.afficher_info("Vous n'avez aucune categorie pour le moment.")

    id_tache = inserer_tache(id_user, titre, description, date_echeance or None, priorite, id_categorie)
    if id_tache:
        affichage.afficher_succes(f"Tache '{titre}' ajoutee (id {id_tache}).")
    else:
        affichage.afficher_erreur("L'ajout de la tache a echoue.")


# ---------- F05 - Lister toutes les taches ----------

def lister_taches(id_user):
    """
    Retourne la liste des taches de l'utilisateur,
    triees par priorite decroissante puis date d'echeance croissante.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s
            ORDER BY
                CASE t.priorite
                    WHEN 'urgente' THEN 1
                    WHEN 'haute' THEN 2
                    WHEN 'normale' THEN 3
                    WHEN 'basse' THEN 4
                END ASC,
                t.date_echeance ASC
        """
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de la recuperation des taches : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_lister_taches(id_user):
    taches = lister_taches(id_user)
    if taches is not None:
        affichage.afficher_liste_taches(taches)


# ---------- F06 - Voir le detail d'une tache ----------

def obtenir_tache(id_tache, id_user):
    """
    Retourne le dict complet d'une tache (avec nom_categorie),
    seulement si elle appartient a id_user. None sinon.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_tache = %s AND t.id_user = %s
        """
        cursor.execute(sql, (id_tache, id_user))
        return cursor.fetchone()
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def obtenir_etiquettes_tache(id_tache):
    """Retourne la liste des etiquettes associees a une tache."""
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return []
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT e.* FROM ETIQUETTE e
            JOIN TACHE_ETIQUETTE te ON e.id_etiquette = te.id_etiquette
            WHERE te.id_tache = %s
        """
        cursor.execute(sql, (id_tache,))
        return cursor.fetchall()
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_detail_tache(id_user):
    print("\n--- Detail d'une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    affichage.afficher_tache(tache)
    etiquettes = obtenir_etiquettes_tache(tache["id_tache"])
    affichage.afficher_etiquettes(etiquettes)


# ---------- F07 - Modifier une tache ----------

def modifier_tache(id_tache, id_user, titre, description, date_echeance, priorite, id_categorie):
    """
    Met a jour une tache existante. Seuls les champs non None sont modifies
    (la logique de 'champ vide = inchange' est geree dans menu_modifier_tache).
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        sql = """
            UPDATE TACHE
            SET titre = %s, description = %s, date_echeance = %s,
                priorite = %s, id_categorie = %s
            WHERE id_tache = %s AND id_user = %s
        """
        valeurs = (titre, description, date_echeance, priorite, id_categorie, id_tache, id_user)
        cursor.execute(sql, valeurs)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de la modification : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_modifier_tache(id_user):
    print("\n--- Modifier une tache ---")
    id_tache = input("Identifiant de la tache a modifier : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    affichage.afficher_info("Valeurs actuelles :")
    affichage.afficher_tache(tache)

    print("\nLaissez un champ vide pour ne pas le modifier.")
    nouveau_titre = input(f"Titre [{tache['titre']}] : ").strip()
    nouvelle_description = input(f"Description [{tache.get('description') or ''}] : ").strip()
    nouvelle_echeance = input(f"Echeance [{tache.get('date_echeance') or ''}] : ").strip()
    nouvelle_priorite = input(f"Priorite [{tache['priorite']}] : ").strip().lower()

    titre_final = nouveau_titre or tache["titre"]
    description_final = nouvelle_description or tache.get("description")
    echeance_final = nouvelle_echeance or tache.get("date_echeance")
    priorite_final = nouvelle_priorite if nouvelle_priorite in ("basse", "normale", "haute", "urgente") else tache["priorite"]
    id_categorie_final = tache.get("id_categorie")

    from categorie import lister_categories
    categories = lister_categories(id_user)
    if categories:
        print("\nVos categories :")
        for c in categories:
            print(f"  {c['id_categorie']}. {c['nom_categorie']}")
        choix = input(f"Nouvelle categorie (vide = inchangee) : ").strip()
        if choix.isdigit():
            id_categorie_final = int(choix)

    succes = modifier_tache(
        int(id_tache), id_user, titre_final, description_final,
        echeance_final, priorite_final, id_categorie_final
    )
    if succes:
        affichage.afficher_succes("Tache modifiee avec succes.")
    else:
        affichage.afficher_erreur("La modification a echoue.")


# ---------- F08 - Changer le statut d'une tache ----------

def changer_statut_tache(id_tache, id_user, nouveau_statut, ancien_statut, commentaire=None):
    """
    Met a jour le statut d'une tache ET enregistre le changement dans HISTORIQUE.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()

        sql_update = "UPDATE TACHE SET statut = %s WHERE id_tache = %s AND id_user = %s"
        cursor.execute(sql_update, (nouveau_statut, id_tache, id_user))

        if cursor.rowcount == 0:
            conn.rollback()
            return False

        sql_historique = """
            INSERT INTO HISTORIQUE (id_tache, ancien_statut, nouveau_statut, commentaire)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_historique, (id_tache, ancien_statut, nouveau_statut, commentaire))

        conn.commit()
        return True
    except Error as e:
        if conn:
            conn.rollback()
        affichage.afficher_erreur(f"Erreur lors du changement de statut : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_changer_statut(id_user):
    print("\n--- Changer le statut d'une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    affichage.afficher_info(f"Statut actuel : {tache['statut']}")
    print("Statuts disponibles : a_faire / en_cours / terminee / annulee")
    nouveau_statut = input("Nouveau statut : ").strip().lower()

    if nouveau_statut not in ("a_faire", "en_cours", "terminee", "annulee"):
        affichage.afficher_erreur("Statut invalide.")
        return

    commentaire = input("Commentaire (optionnel) : ").strip() or None

    succes = changer_statut_tache(int(id_tache), id_user, nouveau_statut, tache["statut"], commentaire)
    if succes:
        affichage.afficher_succes(f"Statut mis a jour : {tache['statut']} -> {nouveau_statut}")
    else:
        affichage.afficher_erreur("Le changement de statut a echoue.")


# ---------- F09 - Supprimer une tache ----------

def supprimer_tache(id_tache, id_user):
    """
    Supprime une tache. Grace a ON DELETE CASCADE, les lignes liees dans
    HISTORIQUE et TACHE_ETIQUETTE sont supprimees automatiquement.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        sql = "DELETE FROM TACHE WHERE id_tache = %s AND id_user = %s"
        cursor.execute(sql, (id_tache, id_user))
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


def menu_supprimer_tache(id_user):
    print("\n--- Supprimer une tache ---")
    id_tache = input("Identifiant de la tache : ").strip()
    if not id_tache.isdigit():
        affichage.afficher_erreur("Identifiant invalide.")
        return

    tache = obtenir_tache(int(id_tache), id_user)
    if tache is None:
        affichage.afficher_erreur("Tache introuvable.")
        return

    confirmation = input(f"Supprimer '{tache['titre']}' ? (o/n) : ").strip().lower()
    if confirmation == "o":
        succes = supprimer_tache(int(id_tache), id_user)
        if succes:
            affichage.afficher_succes("Tache supprimee.")
        else:
            affichage.afficher_erreur("La suppression a echoue.")
    else:
        affichage.afficher_info("Suppression annulee.")