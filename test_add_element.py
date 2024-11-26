import sqlite3

def ajouter_parent(nom, prenom):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parents (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

def ajouter_enfant(nom, prenom):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO enfants (nom, prenom) VALUES (?, ?)', (nom, prenom))
    conn.commit()
    conn.close()

def lier_parent_enfant(parent_id, enfant_id):
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('INSERT INTO parent_enfant (parent_id, enfant_id) VALUES (?, ?)', (parent_id, enfant_id))
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
    conn.close()
    return enfants

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('association.db')
c = conn.cursor()

# Création des tables
c.execute('''
    CREATE TABLE IF NOT EXISTS parents (
        parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        age INTEGER,
        adresse TEXT NOT NULL,
        code_postal TEXT NOT NULL,
        ville TEXT NOT NULL,
        telephone TEXT,
        mail TEXT,
        type TEXT NOT NULL,
        activite TEXT,
        cotisation TEXT NOT NULL,
        montant REAL NOT NULL,
        don REAL,
        mode_paiement TEXT NOT NULL,
        membre_ca BOOLEAN NOT NULL,
        recevoir_entre_nous BOOLEAN NOT NULL,
        date_paiement DATE,
        commentaire TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS enfants (
        enfant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        age INTEGER,
        adresse TEXT NOT NULL,
        code_postal TEXT NOT NULL,
        ville TEXT NOT NULL,
        telephone TEXT,
        mail TEXT,
        type TEXT NOT NULL,
        activite TEXT,
        cotisation TEXT NOT NULL,
        montant REAL NOT NULL,
        don REAL,
        membre_ca BOOLEAN NOT NULL,
        recevoir_entre_nous BOOLEAN NOT NULL,
        date_paiement DATE,
        commentaire TEXT
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

def add_user():
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




