import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Par défaut sous XAMPP, pas de mot de passe
        password="",
        database="jardin_connecte"
    )
