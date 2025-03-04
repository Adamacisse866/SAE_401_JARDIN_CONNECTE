from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user_by_username, get_user_by_email
from flask import Flask
import mysql.connector
from database import get_connection  # Importer la fonction de connexion

#Initialisation de l'application Flask et de Flask-Login
app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager() # Gère les sessions de connexion des utilisateurs.
login_manager.init_app(app)

# Classe User pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
    
    @staticmethod
    def get(user_id):
        # Cette fonction sera utilisée par Flask-Login pour obtenir l'utilisateur
        user = get_user_by_username(user_id)  # Ici, tu récupères l'utilisateur par son ID
        if user:
            return User(user['id'], user['username'], user['email'], user['role'])
        return None

login_manager.user_loader(User.get)

# Fonction pour l'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Crypter le mot de passe

        # Vérifier si l'utilisateur existe déjà
        if get_user_by_username(username):
            flash('Nom d\'utilisateur déjà pris.')
            return redirect(url_for('signup'))
        
        if get_user_by_email(email):
            flash('Email déjà utilisé.')
            return redirect(url_for('signup'))
        # Ajouter l'utilisateur à la base de données
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO utilisateurs (username, email, password, role) VALUES (%s, %s, %s, %s)", 
                       (username, email, hashed_password, 'user'))
        connection.commit()
        connection.close()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Fonction pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['email'], user['role'])
            login_user(user_obj)
            flash('Connexion réussie !')
            return redirect(url_for('home'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.')

    return render_template('login.html')

# Fonction pour la déconnexion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.')
    return redirect(url_for('login'))

# Exemple de page protégée par login
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Accès interdit, vous devez être administrateur.')
        return redirect(url_for('home'))
    return render_template('home_admin.html')

# Fonction pour récupérer les plantes depuis la base de données
def get_plantes():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM plantes")  # Récupérer toutes les plantes
            result = cursor.fetchall()  # Récupérer les résultats
            return result
        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des données : {err}")
            return []
        finally:
            connection.close()  # Fermer la connexion
    else:
        return []

@app.route('/')
def home():
    plantes = get_plantes()  # Récupérer les plantes
    return render_template('home.html', plantes=plantes)

if __name__ == "__main__":
    app.run(debug=True)
