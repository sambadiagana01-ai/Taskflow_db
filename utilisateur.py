# utilisateur.py
import hashlib
from mysql.connector import Error
from connexion import obtenir_connexion, fermer_connexion
import affichage


# ---------- Hashage du mot de passe ----------

def hasher_mdp(mot_de_passe):
    """Retourne le hash SHA-256 du mot de passe."""
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()


def verifier_mdp(mot_de_passe_saisi, hash_stocke):
    """Retourne True si le mot de passe correspond au hash."""
    return hasher_mdp(mot_de_passe_saisi) == hash_stocke


# ---------- F01 - Inscription ----------

def nom_utilisateur_existe(nom_utilisateur):
    """Verifie si un nom d'utilisateur est deja pris."""
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id_user FROM UTILISATEUR WHERE nom_utilisateur = %s"
        cursor.execute(sql, (nom_utilisateur,))
        resultat = cursor.fetchone()
        return resultat is not None
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def inscrire_utilisateur(nom_utilisateur, email, mot_de_passe):
    """
    Insere un nouvel utilisateur dans la base.
    Retourne True si l'inscription a reussi, False sinon.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return False
        cursor = conn.cursor()
        mdp_hashe = hasher_mdp(mot_de_passe)
        sql = """INSERT INTO UTILISATEUR (nom_utilisateur, email, mot_de_passe)
                 VALUES (%s, %s, %s)"""
        cursor.execute(sql, (nom_utilisateur, email, mdp_hashe))
        conn.commit()
        return True
    except Error as e:
        affichage.afficher_erreur(f"Erreur lors de l'inscription : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_inscription():
    """
    Gere le flux complet d'inscription depuis le terminal.
    Retourne le dict utilisateur cree, ou None si echec.
    """
    print("\n--- Inscription ---")
    nom_utilisateur = input("Nom d'utilisateur : ").strip()

    if not nom_utilisateur:
        affichage.afficher_erreur("Le nom d'utilisateur ne peut pas etre vide.")
        return None

    existe = nom_utilisateur_existe(nom_utilisateur)
    if existe is None:
        return None
    if existe:
        affichage.afficher_erreur("Ce nom d'utilisateur est deja pris.")
        return None

    email = input("Email : ").strip()
    mdp1 = input("Mot de passe : ").strip()
    mdp2 = input("Confirmez le mot de passe : ").strip()

    if mdp1 != mdp2:
        affichage.afficher_erreur("Les mots de passe ne correspondent pas.")
        return None

    if len(mdp1) < 4:
        affichage.afficher_erreur("Le mot de passe doit contenir au moins 4 caracteres.")
        return None

    succes = inscrire_utilisateur(nom_utilisateur, email, mdp1)
    if succes:
        affichage.afficher_succes(f"Inscription reussie ! Bienvenue {nom_utilisateur}.")
        return connecter_utilisateur(nom_utilisateur, mdp1)
    else:
        affichage.afficher_erreur("L'inscription a echoue.")
        return None


# ---------- F02 - Connexion ----------

def connecter_utilisateur(nom_utilisateur, mot_de_passe):
    """
    Verifie les identifiants et retourne le dict utilisateur si valide,
    None sinon.
    """
    conn = None
    cursor = None
    try:
        conn = obtenir_connexion()
        if conn is None:
            return None
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM UTILISATEUR WHERE nom_utilisateur = %s"
        cursor.execute(sql, (nom_utilisateur,))
        utilisateur = cursor.fetchone()

        if utilisateur is None:
            return None

        if verifier_mdp(mot_de_passe, utilisateur["mot_de_passe"]):
            return utilisateur
        else:
            return None
    except Error as e:
        affichage.afficher_erreur(f"Erreur base de donnees : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)


def menu_connexion():
    """
    Gere le flux complet de connexion depuis le terminal.
    Retourne le dict utilisateur connecte, ou None si echec.
    """
    print("\n--- Connexion ---")
    nom_utilisateur = input("Nom d'utilisateur : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()

    utilisateur = connecter_utilisateur(nom_utilisateur, mot_de_passe)
    if utilisateur:
        affichage.afficher_succes(f"Connexion reussie. Bienvenue {utilisateur['nom_utilisateur']} !")
        return utilisateur
    else:
        affichage.afficher_erreur("Nom d'utilisateur ou mot de passe incorrect.")
        return None


# ---------- F03 - Deconnexion ----------

def deconnecter_utilisateur():
    """
    Affiche un message de deconnexion.
    La vraie 'suppression' de la session se fait dans main.py
    en remettant la variable utilisateur_connecte a None.
    """
    affichage.afficher_info("Vous etes deconnecte.")