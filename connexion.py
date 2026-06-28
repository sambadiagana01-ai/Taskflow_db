# connexion.py

import mysql.connector
from mysql.connector import Error

# Informations de connexion à adapter selon votre configuration
CONFIG = {
    "host": "localhost",       # adresse du serveur MySQL
    "user": "root",            # nom d'utilisateur MySQL
    "password": "",            # mot de passe MySQL
    "database": "taskflow_db", # nom de la base de données
    "charset": "utf8mb4"
}

def obtenir_connexion():
    """
    Ouvre et retourne une connexion à la base de données.
    Retourne None si la connexion échoue.
    """
    try:
        conn = mysql.connector.connect(**CONFIG)

        if conn.is_connected():
            print("Connexion à la base de données réussie.")
            return conn

    except Error as e:
        print(f"Erreur de connexion : {e}")
        return None


def fermer_connexion(conn):
    """
    Ferme proprement la connexion si elle est ouverte.
    """
    if conn is not None and conn.is_connected():
        conn.close()
        print("Connexion fermée.")