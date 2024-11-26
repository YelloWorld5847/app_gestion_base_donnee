import sqlite3
from faker import Faker
import random


def remplir_utilisateurs(conn, nombre_utilisateurs):
    cursor = conn.cursor()
    fake = Faker('fr_FR')  # Utiliser le locale français pour des données réalistes

    for _ in range(nombre_utilisateurs):
        nom = fake.last_name()
        prenom = fake.first_name()
        annee_naissance = random.randint(1920, 2023)
        adresse = fake.address().replace('\n', ', ')
        code_postal = ''.join(str(random.randint(0, 9)) for _ in range(5))
        ville = fake.city()
        telephone = f"0{''.join(str(random.randint(0, 9)) for _ in range(9))}"  #fake.phone_number().replace(' ', '').replace('+33', '0')
        if len(telephone) != 10:
            print(len(telephone))
        mail = fake.email()
        type_utilisateur = random.choice(['Adhérent', 'Membre', 'Bénévole'])
        activite = fake.job()
        cotisation = 2023 #random.randint(1990, 2023)
        montant = round(random.uniform(10.0, 500.0), 2)
        don = round(random.uniform(0.0, 1000.0), 2)
        mode_paiement = random.choice(['Carte Bancaire', 'Chèque', "eloasso"])
        membre_ca = random.choice([True, False])
        recevoir_entre_nous = random.choice([True, False])
        date_paiement = fake.date_this_decade().strftime('%Y-%m-%d')
        commentaire = fake.text(max_nb_chars=200)

        cursor.execute('''
        INSERT INTO users (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, membre_ca, recevoir_entre_nous, date_paiement, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nom, prenom, annee_naissance, adresse, code_postal, ville, telephone, mail, type_utilisateur, activite,
              cotisation, montant, don, mode_paiement, membre_ca, recevoir_entre_nous, date_paiement, commentaire))

    conn.commit()




def insert_relation(parent_id, child_id):
    conn = sqlite3.connect('association.db')
    cursor.execute('INSERT INTO relations (parent_id, child_id) VALUES (?, ?)', (parent_id, child_id))
    conn.commit()

# Connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('association.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    age INTEGER,
    adresse TEXT,
    code_postal TEXT,
    ville TEXT,
    telephone TEXT,
    mail TEXT,
    type TEXT,
    activite TEXT,
    cotisation TEXT,
    montant REAL,
    don REAL,
    mode_paiement TEXT,
    membre_ca BOOLEAN,
    recevoir_entre_nous BOOLEAN,
    date_paiement DATE,
    commentaire TEXT
)
''')

# Création de la table des relations parent-enfant
cursor.execute('''
CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    child_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES users(id),
    FOREIGN KEY (child_id) REFERENCES users(id)
)
''')

# Création de la table pour enregistrer les nom des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS name_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    relation TEXT
)
''')


conn.commit()

# # Insertion des utilisateurs
# john_id = insert_user('John')
# jane_id = insert_user('Jane')
# joe_id = insert_user('Joe')
# jill_id = insert_user('Jill')
#
# # Insertion des relations parent-enfant
# insert_relation(john_id, joe_id)  # John est le parent de Joe
# insert_relation(jane_id, joe_id)  # Jane est le parent de Joe
# insert_relation(john_id, jill_id)  # John est le parent de Jill
# insert_relation(jane_id, jill_id)  # Jane est le parent de Jill


def get_children(parent_id):
    cursor.execute('''
    SELECT users.id, users.name FROM users
    JOIN relations ON users.id = relations.child_id
    WHERE relations.parent_id = ?
    ''', (parent_id,))
    return cursor.fetchall()

def get_parents(child_id):
    cursor.execute('''
    SELECT users.id, users.name FROM users
    JOIN relations ON users.id = relations.parent_id
    WHERE relations.child_id = ?
    ''', (child_id,))
    return cursor.fetchall()

def get_siblings(user_id):
    cursor.execute('''
    SELECT siblings.id, siblings.name FROM users AS siblings
    JOIN relations AS r1 ON siblings.id = r1.child_id
    JOIN relations AS r2 ON r1.parent_id = r2.parent_id
    WHERE r2.child_id = ? AND siblings.id != ?
    ''', (user_id, user_id))
    return cursor.fetchall()

# # Exemple d'utilisation
# print("Children of John:", get_children(john_id))
# print("Parents of Joe:", get_parents(joe_id))
# print("Siblings of Joe:", get_siblings(joe_id))

# Connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('association.db')

# Remplissage de la table des utilisateurs avec 10 utilisateurs valides
remplir_utilisateurs(conn, 70)

# Fermeture de la connexion
conn.close()