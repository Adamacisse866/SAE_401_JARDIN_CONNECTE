# models/event.py
from datetime import datetime
from config import db

class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50), nullable=False)  # Date en format string ou datetime
    image_url = db.Column(db.String(255), nullable=False)  # URL de l'image de fond
    link = db.Column(db.String(255), nullable=True)  # Lien optionnel pour certains événements

    def __repr__(self):
        return f"<Event {self.title}>"
