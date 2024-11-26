from cryptography.fernet import Fernet
import sqlite3
import os

# Générer une clé et l'enregistrer dans un fichier
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

def ajouter_parent(nom, prenom):
    conn = sqlite3.connect('decrypted_famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

def ajouter_enfant(nom, prenom):
    conn = sqlite3.connect('decrypted_famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

def lier_parent_enfant(parent_id, enfant_id):
    conn = sqlite3.connect('decrypted_famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
    conn.commit()
    conn.close()

def obtenir_enfants(parent_id):
    conn = sqlite3.connect('decrypted_famille.db')
    c = conn.cursor()
    c.execute('''
        SELECT enfants.enfant_id, enfants.nom, enfants.prenom
        FROM enfants
        INNER JOIN parent_enfant ON enfants.enfant_id = parent_enfant.enfant_id
        WHERE parent_enfant.parent_id = ?
    ''', (parent_id,))
    enfants = c.fetchall()
    conn.close()
    return enfants

# Fonction pour récupérer le parent_id à partir du nom et prénom
def get_parent_id(nom, prenom):
    conn = sqlite3.connect('decrypted_famille.db')
    c = conn.cursor()
    c.execute('SELECT parent_id FROM parents WHERE nom = ? AND prenom = ?', (nom, prenom))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('famille.db')
c = conn.cursor()

# Création des tables
c.execute('''
    CREATE TABLE IF NOT EXISTS parents (
        parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS enfants (
        enfant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS parent_enfant (
        parent_id INTEGER,
        enfant_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES parents (parent_id),
        FOREIGN KEY (enfant_id) REFERENCES enfants (enfant_id)
    )
''')

# Validation des changements
conn.commit()
conn.close()



def encrypt_data(base_donne):
    # Charger la clé de chiffrement
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()

    # Initialiser Fernet avec la clé
    cipher_suite = Fernet(key)

    # Lire le contenu de la base de données
    with open(base_donne, 'rb') as db_file:
        db_data = db_file.read()

    # Chiffrer les données de la base de données
    encrypted_db_data = cipher_suite.encrypt(db_data)

    # Enregistrer les données chiffrées dans un fichier
    with open('encrypted_famille.db', 'wb') as enc_db_file:
        enc_db_file.write(encrypted_db_data)

def decrypt_data(base_donne):
    # Charger la clé de chiffrement
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()

    # Initialiser Fernet avec la clé
    cipher_suite = Fernet(key)

    # Lire les données chiffrées de la base de données
    with open(base_donne, 'rb') as enc_db_file:
        encrypted_db_data = enc_db_file.read()

    # Déchiffrer les données de la base de données
    decrypted_db_data = cipher_suite.decrypt(encrypted_db_data)

    # Enregistrer les données déchiffrées dans un fichier temporaire
    with open('decrypted_famille.db', 'wb') as dec_db_file:
        dec_db_file.write(decrypted_db_data)

    # Connexion à la base de données déchiffrée et lecture des données
    conn = sqlite3.connect('decrypted_famille.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM parents''')
    parents = cursor.fetchall()
    for parent in parents:
        print(f'Parent ID: {parent[0]}, Nom: {parent[1]}, Prénom: {parent[2]}')
    conn.close()

encrypt_data('famille.db')
decrypt_data('encrypted_famille.db')

def add_user():
    ajouter_parent('Dupont', 'Jean')
    ajouter_parent('Dupont', 'Marie')
    ajouter_enfant('Dupont', 'Pierre')
    ajouter_enfant('Dupont', 'Julie')

    # Supposons que les IDs des parents et des enfants sont les suivants:
    # Jean Dupont (parent_id=1), Marie Dupont (parent_id=2)
    # Pierre Dupont (enfant_id=1), Julie Dupont (enfant_id=2)

    lier_parent_enfant(get_parent_id("Dupont", "Jean"), get_parent_id("Dupont", "Pierre"))  # Jean est parent de Pierre
    lier_parent_enfant(2, 1)  # Marie est parent de Pierre
    lier_parent_enfant(1, 2)  # Jean est parent de Julie
    lier_parent_enfant(2, 2)  # Marie est parent de Julie

add_user()

encrypt_data('decrypted_famille.db')

# Optionnel: Supprimer le fichier de base de données déchiffré après usage
os.remove('decrypted_famille.db')