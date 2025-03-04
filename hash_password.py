from werkzeug.security import generate_password_hash

mot_de_passe = "admin123"  # Mets ici le mot de passe que tu veux pour l'admin
hashed_password = generate_password_hash(mot_de_passe)

print("Mot de passe haché :", hashed_password)
