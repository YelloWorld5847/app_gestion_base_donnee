import sqlite3

# Connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('utilisateur_relation.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Création de la table des relations parent-enfant
cursor.execute('''
CREATE TABLE IF NOT EXISTS relations (
    parent_id INTEGER,
    child_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES users(id),
    FOREIGN KEY (child_id) REFERENCES users(id)
)
''')

conn.commit()

def insert_user(name):
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()
    return cursor.lastrowid

def insert_relation(parent_id, child_id):
    cursor.execute('INSERT INTO relations (parent_id, child_id) VALUES (?, ?)', (parent_id, child_id))
    conn.commit()

# Insertion des utilisateurs
john_id = insert_user('John')
jane_id = insert_user('Jane')
joe_id = insert_user('Joe')
jill_id = insert_user('Jill')

# Insertion des relations parent-enfant
insert_relation(john_id, joe_id)  # John est le parent de Joe
insert_relation(jane_id, joe_id)  # Jane est le parent de Joe
insert_relation(john_id, jill_id)  # John est le parent de Jill
insert_relation(jane_id, jill_id)  # Jane est le parent de Jill


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
    SELECT DISTINCT siblings.id, siblings.name 
    FROM users AS siblings
    JOIN relations AS r1 ON siblings.id = r1.child_id
    JOIN relations AS r2 ON r1.parent_id = r2.parent_id
    WHERE r2.child_id = ? AND siblings.id != ?
    ''', (user_id, user_id))
    return cursor.fetchall()

# Exemple d'utilisation
print("Children of John:", get_children(john_id))
print("Parents of Joe:", get_parents(joe_id))
print("Siblings of Joe:", get_siblings(joe_id))
