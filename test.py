from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import sqlite3
import shutil
from datetime import datetime

# Fonction pour chiffrer les données
def encrypt_data(data, password):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(password.encode()), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

# Fonction pour déchiffrer les données
def decrypt_data(encrypted_data, password):
    backend = default_backend()
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(password.encode()), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data

# Fonction pour créer une sauvegarde de la base de données
def sauvegarder_base_de_donnees():
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Créer une copie de la base de données avec un horodatage
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = os.path.join(backup_dir, f'famille_{timestamp}.db')
    shutil.copyfile(db_path, backup_path)

    # Gérer le nombre de sauvegardes pour conserver uniquement les 10 dernières
    backups = sorted(os.listdir(backup_dir))
    if len(backups) > max_backups:
        oldest_backup = backups[0]
        os.remove(os.path.join(backup_dir, oldest_backup))

def ajouter_parent(nom, prenom):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    close_db(conn)

    # Effectuer une sauvegarde après avoir ajouté un parent
    sauvegarder_base_de_donnees()

def ajouter_enfant(nom, prenom):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    close_db(conn)

    # Effectuer une sauvegarde après avoir ajouté un parent
    sauvegarder_base_de_donnees()

def lier_parent_enfant(parent_id, enfant_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
    conn.commit()
    close_db(conn)

def obtenir_enfants(parent_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        SELECT enfants.enfant_id, enfants.nom, enfants.prenom
        FROM enfants
        INNER JOIN parent_enfant ON enfants.enfant_id = parent_enfant.enfant_id
        WHERE parent_enfant.parent_id = ?
    ''', (parent_id,))
    enfants = c.fetchall()
    close_db(conn)
    return enfants

# Fonction pour établir une connexion à la base de données
def connect_db():
    try:
        # Lecture du contenu chiffré de la base de données
        with open(db_path, 'rb') as f:
            encrypted_content = f.read()

        # Déchiffrement du contenu
        decrypted_content = decrypt_data(encrypted_content, password)

        # Écriture du contenu déchiffré dans un fichier temporaire
        temp_db_path = 'temp_famille.db'
        with open(temp_db_path, 'wb') as f:
            f.write(decrypted_content)

        # Connexion à la base de données déchiffrée
        conn = sqlite3.connect(temp_db_path)
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")

# Fonction pour fermer la connexion à la base de données
def close_db(conn):
    try:
        # Fermeture de la connexion
        conn.close()

        # Lecture du contenu de la base de données temporaire
        with open('temp_famille.db', 'rb') as f:
            plain_content = f.read()

        # Chiffrement du contenu
        encrypted_content = encrypt_data(plain_content, password)

        # Écriture du contenu chiffré dans le fichier de base de données
        with open(db_path, 'wb') as f:
            f.write(encrypted_content)

        # Suppression du fichier temporaire
        os.remove('temp_famille.db')
    except Exception as e:
        print(f"Erreur lors de la fermeture de la base de données : {e}")

# Variables globales pour le chemin de la base de données et le mot de passe
db_path = 'famille2.db'
password = os.getenv('ENCRYPTION_KEY')

# Assurez-vous que le mot de passe est de la bonne longueur (16, 24, ou 32 octets pour AES)
if len(password) not in [16, 24, 32]:
    raise ValueError("La clé de chiffrement doit être de 16, 24 ou 32 octets de longueur.")

backup_dir = 'backups'
max_backups = 10

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Création de la table parents
c.execute('''
    CREATE TABLE IF NOT EXISTS parents (
        parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    )
''')

# Création de la table enfants
c.execute('''
    CREATE TABLE IF NOT EXISTS enfants (
        enfant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    )
''')

# Création de la table de liaison parent_enfant
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

# Fermeture de la connexion
conn.close()

def add_user():
    # Exemple d'utilisation
    ajouter_parent('Dupont', 'Jean')
    ajouter_parent('Dupont', 'Marie')
    ajouter_enfant('Dupont', 'Pierre')
    ajouter_enfant('Dupont', 'Julie')

    lier_parent_enfant(1, 1)
    lier_parent_enfant(2, 1)
    lier_parent_enfant(1, 2)
    lier_parent_enfant(2, 2)

add_user()

# Exemple d'utilisation
enfants_de_jean = obtenir_enfants(1)
for enfant in enfants_de_jean:
    print(f'ID: {enfant[0]}, Nom: {enfant[1]}, Prénom: {enfant[2]}')

sauvegarder_base_de_donnees()
