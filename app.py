from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="jardin_connecte"
)
cursor = conn.cursor(dictionary=True)

@app.route("/events", methods=["GET"])
def get_events():
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    # Convertir l'heure (timedelta) en format lisible "HH:MM:SS"
    for event in events:
        if isinstance(event["heure"], str) == False:  # Vérifie si c'est bien un timedelta
            event["heure"] = str(event["heure"])  # Convertir timedelta en string

    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
