from config import db

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Médicinale, Potagère...
    status = db.Column(db.String(50), nullable=False)  # Floraison, Récolte...
    description = db.Column(db.Text)
