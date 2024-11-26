from cryptography.fernet import Fernet

# Charger la clé de chiffrement
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

# Lire le contenu de la base de données
with open('famille.db', 'rb') as db_file:
    db_data = db_file.read()

# Chiffrer les données de la base de données
encrypted_db_data = cipher_suite.encrypt(db_data)

# Enregistrer les données chiffrées dans un fichier
with open('encrypted_famille.db', 'wb') as enc_db_file:
    enc_db_file.write(encrypted_db_data)
