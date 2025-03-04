from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = "mysql+pymysql://root:@localhost/jardin_connecte"  # Mets ici le bon nom de ta base de données

db = SQLAlchemy()
