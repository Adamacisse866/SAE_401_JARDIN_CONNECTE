from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "secretkey123"  # Clé secrète pour Flask sessions

# 📌 Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Remplace par ton user MySQL si différent
app.config['MYSQL_PASSWORD'] = ''  # Mot de passe MySQL (laisser vide si XAMPP par défaut)
app.config['MYSQL_DB'] = 'jardin_connecte'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 📌 Classe User pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user["id"], user["username"], user["role"])
    return None

# 📌 Page d'accueil
@app.route('/')
def home():
    return render_template('login.html')

# 📌 Inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash du mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # FORCER le rôle "user" pour empêcher la création d'admin
        role = 'user'

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        mysql.connection.commit()
        cur.close()

        flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# 📌 Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(user["id"], user["username"], user["role"])
            login_user(user_obj)

            flash('Connexion réussie !', 'success')
            if user["role"] == "admin":
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('user_home'))
        else:
            flash('Identifiants incorrects.', 'danger')

    return render_template('login.html')

# 📌 Page d'accueil Admin
@app.route('/admin/home')
@login_required
def admin_home():
    if current_user.role != 'admin':
        flash("Accès refusé !", "danger")
        return redirect(url_for('home'))
    return render_template('home_admin.html')

# 📌 Page d'accueil User
@app.route('/user/home')
@login_required
def user_home():
    if current_user.role != 'user':
        flash("Accès refusé !", "danger")
        return redirect(url_for('home'))
    return render_template('home_user.html')

# 📌 Déconnexion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie !", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
