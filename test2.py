import sqlite3
from cryptography.fernet import Fernet
import os
# Générer une clé et l'enregistrer dans un fichier
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)

key = "mXvnVSJzWhPue00K3fKtf-LFCpZ-TBsp5YyOprzcdqY="
print(len(key))
# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

# Créer une base de données SQLite et ajouter des données
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
cursor.execute('''INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25)''')
conn.commit()
conn.close()

# Lire le contenu de la base de données
with open('example.db', 'rb') as db_file:
    db_data = db_file.read()

# Chiffrer les données de la base de données
encrypted_db_data = cipher_suite.encrypt(db_data)

# Enregistrer les données chiffrées dans un fichier
with open('encrypted_example.db', 'wb') as enc_db_file:
    enc_db_file.write(encrypted_db_data)



# # Charger la clé de chiffrement
# with open('secret.key', 'rb') as key_file:
#     key = key_file.read()

# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

# Lire les données chiffrées de la base de données
with open('encrypted_example.db', 'rb') as enc_db_file:
    encrypted_db_data = enc_db_file.read()

# Déchiffrer les données de la base de données
decrypted_db_data = cipher_suite.decrypt(encrypted_db_data)

# Enregistrer les données déchiffrées dans un fichier temporaire
with open('decrypted_example.db', 'wb') as dec_db_file:
    dec_db_file.write(decrypted_db_data)

# Connexion à la base de données déchiffrée et lecture des données
conn = sqlite3.connect('decrypted_example.db')
cursor = conn.cursor()
cursor.execute('''SELECT * FROM users''')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()

# Optionnel: Supprimer le fichier de base de données déchiffré après usage
os.remove('decrypted_example.db')

