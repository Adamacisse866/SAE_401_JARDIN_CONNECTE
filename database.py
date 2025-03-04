import mysql.connector

# Configuration de la connexion à MySQL
db_config = {
    "host": "localhost",       
    "user": "root",            
    "password": "",            
    "database": "jardin_connecte"  
}

# Fonction pour établir la connexion à la base de données
def get_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None

# fonction pour reccuperer un utilisateur par son nom d'utilisateur
def get_user_by_username(username):
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM utilisateurs WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None

# fonction pour reccuperer un utilisateur par son addresse email
def get_user_by_email(email):
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM utilisateurs WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None
