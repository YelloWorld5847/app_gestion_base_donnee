# from cryptography.fernet import Fernet
import sqlite3

# # Générer une clé et l'enregistrer dans un fichier
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)



def ajouter_parent(nom, prenom):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.commit()
    conn.close()



def ajouter_enfant(nom, prenom):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.commit()
    conn.close()


def lier_parent_enfant(parent_id, enfant_id):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
    conn.commit()
    conn.commit()
    conn.close()

def obtenir_enfants(parent_id):
    conn = sqlite3.connect('famille.db')
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




# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('famille.db')
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

    # Supposons que les IDs des parents et des enfants sont les suivants:
    # Jean Dupont (parent_id=1), Marie Dupont (parent_id=2)
    # Pierre Dupont (enfant_id=1), Julie Dupont (enfant_id=2)

    lier_parent_enfant(1, 1)  # Jean est parent de Pierre
    lier_parent_enfant(2, 1)  # Marie est parent de Pierre
    lier_parent_enfant(1, 2)  # Jean est parent de Julie
    lier_parent_enfant(2, 2)  # Marie est parent de Julie

add_user()


# Exemple d'utilisation
enfants_de_jean = obtenir_enfants(1)
for enfant in enfants_de_jean:
    print(f'ID: {enfant[0]}, Nom: {enfant[1]}, Prénom: {enfant[2]}')


