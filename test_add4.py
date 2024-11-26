from cryptography.fernet import Fernet
import sqlite3
import os
# # Générer une clé et l'enregistrer dans un fichier
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)



def ajouter_parent(nom, prenom):
    conn = sqlite3.connect('decrypted_famille1.db')
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.commit()
    conn.close()

def ajouter_enfant(nom, prenom):
    conn = sqlite3.connect('decrypted_famille1.db')
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.commit()
    conn.close()


def lier_parent_enfant(parent_id, enfant_id):
    conn = sqlite3.connect('decrypted_famille1.db')
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
    conn.commit()
    conn.commit()
    conn.close()

def obtenir_enfants(parent_id):
    conn = sqlite3.connect('decrypted_famille1.db')
    c = conn.cursor()
    c.execute('''
        SELECT enfants.enfant_id, enfants.nom, enfants.prenom
        FROM enfants
        INNER JOIN parent_enfant ON enfants.enfant_id = parent_enfant.enfant_id
        WHERE parent_enfant.parent_id = ?
    ''', (parent_id,))
    enfants = c.fetchall()
    conn.commit()
    conn.close()
    return enfants

def dechiffrer():
    # Lire les données chiffrées de la base de données
    with open('encrypted_famille1.db', 'rb') as enc_db_file:
        encrypted_db_data = enc_db_file.read()

    # Déchiffrer les données de la base de données
    decrypted_db_data = cipher_suite.decrypt(encrypted_db_data)

    print(decrypted_db_data)

    # Enregistrer les données déchiffrées dans un fichier temporaire
    with open('decrypted_famille1.db', 'wb') as dec_db_file:
        dec_db_file.write(decrypted_db_data)

def chiffrer():
    # Rechiffrer la base de données
    with open('decrypted_famille1.db', 'rb') as db_file:
        db_data = db_file.read()

    encrypted_db_data = cipher_suite.encrypt(db_data)

    with open('encrypted_famille1.db', 'wb') as enc_db_file:
        enc_db_file.write(encrypted_db_data)

def afficher_donner():
    # Connexion à la base de données déchiffrée et lecture des données
    conn = sqlite3.connect('decrypted_famille1.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM parents''')
    parents = cursor.fetchall()
    for parent in parents:
        print(f'Parent ID: {parent[0]}, Nom: {parent[1]}, Prénom: {parent[2]}')
    conn.close()

# Charger la clé de chiffrement
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

dechiffrer()
ajouter_parent('TEST', 'Test_p')
afficher_donner()
chiffrer()

os.remove('decrypted_famille1.db')


# def add_user():
#     # Exemple d'utilisation
#     ajouter_parent('Dupont', 'Jean')
#     ajouter_parent('Dupont', 'Marie')
#     ajouter_enfant('Dupont', 'Pierre')
#     ajouter_enfant('Dupont', 'Julie')
#
#     # Supposons que les IDs des parents et des enfants sont les suivants:
#     # Jean Dupont (parent_id=1), Marie Dupont (parent_id=2)
#     # Pierre Dupont (enfant_id=1), Julie Dupont (enfant_id=2)
#
#     lier_parent_enfant(1, 1)  # Jean est parent de Pierre
#     lier_parent_enfant(2, 1)  # Marie est parent de Pierre
#     lier_parent_enfant(1, 2)  # Jean est parent de Julie
#     lier_parent_enfant(2, 2)  # Marie est parent de Julie
#
# add_user()
#
#
# # Exemple d'utilisation
# enfants_de_jean = obtenir_enfants(1)
# for enfant in enfants_de_jean:
#     print(f'ID: {enfant[0]}, Nom: {enfant[1]}, Prénom: {enfant[2]}')


