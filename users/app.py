from flask import Flask, render_template
from config import db, DATABASE_URI
from sqlalchemy import text
from models.user import User  # Assure-toi d'importer tous tes modèles
from models.plant import Plant
from models.event import Event
from models.idea import Idea
from flask_cors import CORS
from routes.event_routes import event_routes


app = Flask(__name__)
CORS(app)
app.register_blueprint(event_routes)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#mYancheng modifi ! les routes pour acceder les pages diffirents
@app.route("/home")
def index():
    # Rendre le fichier index.html depuis le dossier templates
    return render_template('index.html', active_nav='home')

@app.route('/apprentissage')
def apprentissage():
    return render_template('apprentissage.html', active_nav='apprentissage')

@app.route('/communaute')
def communaute():
    return render_template('communaute.html', active_nav='communaute')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html', active_nav='scanner')


@app.route("/test-db")
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}

# ✅ Ajout de la création des tables après l'import des modèles
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
