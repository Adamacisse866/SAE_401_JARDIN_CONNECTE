from flask import Flask
from users.app import users_app
from admin.app import admin_app

app = Flask(__name__)

app.register_blueprint(users_app, url_prefix='/users')
app.register_blueprint(admin_app, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)