from cryptography.fernet import Fernet
import sqlite3
import os

# Charger la clé de chiffrement
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

def dechiffrer():
    # Lire les données chiffrées de la base de données
    with open('encrypted_famille3.db', 'rb') as enc_db_file:
        encrypted_db_data = enc_db_file.read()

    # Déchiffrer les données de la base de données
    decrypted_db_data = cipher_suite.decrypt(encrypted_db_data)

    # Enregistrer les données déchiffrées dans un fichier temporaire
    with open('decrypted_famille2.db', 'wb') as dec_db_file:
        dec_db_file.write(decrypted_db_data)

dechiffrer()

# # Connexion à la base de données déchiffrée et lecture des données
# conn = sqlite3.connect('decrypted_famille2.db')
# cursor = conn.cursor()
# cursor.execute('''SELECT * FROM parents''')
# parents = cursor.fetchall()
# for parent in parents:
#     print(f'Parent ID: {parent[0]}, Nom: {parent[1]}, Prénom: {parent[2]}')
# conn.close()



# Optionnel: Supprimer le fichier de base de données déchiffré après usage
#os.remove('decrypted_famille.db')

def ajouter_parent(nom, prenom):
    conn = sqlite3.connect('decrypted_famille2.db')
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

ajouter_parent('TEST', 'Test_p')
def afficher_donner():
    # Connexion à la base de données déchiffrée et lecture des données
    conn = sqlite3.connect('decrypted_famille2.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM parents''')
    parents = cursor.fetchall()
    for parent in parents:
        print(f'Parent ID: {parent[0]}, Nom: {parent[1]}, Prénom: {parent[2]}')
    conn.close()
afficher_donner()

def ajouter_enfant(nom, prenom):
    conn = sqlite3.connect('decrypted_famille2.db')
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

def lier_parent_enfant(parent_id, enfant_id):
    conn = sqlite3.connect('decrypted_famille2.db')
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
    conn.commit()
    conn.close()

def obtenir_enfants(parent_id):
    conn = sqlite3.connect('decrypted_famille2.db')
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

def add_and_encrypt_new_data():
    # Déchiffrer la base de données
    with open('encrypted_famille.db', 'rb') as enc_db_file:
        encrypted_db_data = enc_db_file.read()

    decrypted_db_data = cipher_suite.decrypt(encrypted_db_data)

    with open('decrypted_famille.db', 'wb') as dec_db_file:
        dec_db_file.write(decrypted_db_data)

    # Ajouter des éléments
    ajouter_parent('TEST', 'Test_p')
    ajouter_enfant('TEST', 'Test_e')
    #lier_parent_enfant(3, 3)  # Supposons que les IDs sont corrects

    # Rechiffrer la base de données
    with open('decrypted_famille.db', 'rb') as db_file:
        db_data = db_file.read()

    encrypted_db_data = cipher_suite.encrypt(db_data)

    with open('encrypted_famille.db', 'wb') as enc_db_file:
        enc_db_file.write(encrypted_db_data)

    # Supprimer le fichier temporaire
    os.remove('decrypted_famille.db')

    # Connexion à la base de données déchiffrée et lecture des données
    conn = sqlite3.connect('decrypted_famille.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM parents''')
    parents = cursor.fetchall()
    for parent in parents:
        print(f'Parent ID: {parent[0]}, Nom: {parent[1]}, Prénom: {parent[2]}')
    conn.close()


# Utiliser cette fonction pour ajouter des données et les sauvegarder
# add_and_encrypt_new_data()

# Ajouter des éléments
# ajouter_parent('TEST', 'Test_p')
# ajouter_enfant('TEST', 'Test_e')

def chiffrer():
    # Rechiffrer la base de données
    with open('decrypted_famille2.db', 'rb') as db_file:
        db_data = db_file.read()

    encrypted_db_data = cipher_suite.encrypt(db_data)

    with open('encrypted_famille3.db', 'wb') as enc_db_file:
        enc_db_file.write(encrypted_db_data)
chiffrer()

os.remove('decrypted_famille2.db')