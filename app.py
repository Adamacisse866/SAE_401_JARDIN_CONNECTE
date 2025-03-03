from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object("config.Config")

mysql = MySQL(app)

@app.route("/")
def index():
    return "Connexion MySQL réussie Adama !"

@app.route("/events", methods=["GET"])
def get_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    cur.close()
    
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
