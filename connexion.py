# connexion.py
import mysql.connector
from mysql.connector import Error

# Informations de connexion a adapter selon votre configuration
CONFIG = {
    "host": "localhost",       # adresse du serveur MySQL
    "user": "root",            # votre nom d'utilisateur MySQL
    "password": "",  # votre mot de passe MySQL
    "database": "taskflow_db", # nom de la base creee
    "charset": "utf8mb4"
}


def obtenir_connexion():
    """
    Ouvre et retourne une connexion a la base de donnees.
    Retourne None si la connexion echoue.

    Utilisation dans les autres modules :
        conn = obtenir_connexion()
        if conn:
            # faire des requetes
            conn.close()
    """
    try:
        conn = mysql.connector.connect(**CONFIG)
        return conn
    except Error as e:
        print(f"Erreur de connexion a la base de donnees : {e}")
        return None


def fermer_connexion(conn):
    """
    Ferme proprement la connexion si elle est ouverte.
    """
    if conn is not None and conn.is_connected():
        conn.close()


def test_connexion():
    """
    Teste la connexion et affiche un message clair.
    """
    conn = obtenir_connexion()
    if conn:
        print("Connexion reussie !")
        fermer_connexion(conn)
    else:
        print("Echec de la connexion.")


if __name__ == "__main__":
    test_connexion()