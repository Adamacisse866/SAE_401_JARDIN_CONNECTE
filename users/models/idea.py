from config import db

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    idea_text = db.Column(db.Text, nullable=False)
    validated = db.Column(db.Boolean, default=False)
