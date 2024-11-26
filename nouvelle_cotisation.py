# ajout fonctionnalité pour géré chaque nouvelle cotisation

import random
import tkinter as tk
import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from datetime import datetime
import pyperclip
from tkinter import messagebox
import re


possible_end_modif = True

annee_en_cours = 2024 #datetime.now().year
date_en_cours = datetime.now().date()
print(date_en_cours)

# Fonction pour récupérer la longueur du Treeview
def get_treeview_length():
    return len(tableau.get_children())

def copy_data():
    # Crée les nouvelles tables
    nom_user, nom_relations = creat_new_table()

    chargement_meter2 = ttk.Meter(tab4, bootstyle="success", amountused=0, metersize=200, interactive=True,
                                  stripethickness=2, meterthickness=15, textright="%",
                                  subtext="Copie des\nutilisateurs", subtextfont=20)

    chargement_meter2.place(x=180, y=180)

    # Connexion à la base de données source
    conn_src = sqlite3.connect('association.db')
    cursor_src = conn_src.cursor()

    # Lecture des données de la table users
    cursor_src.execute('SELECT * FROM users')
    parents_data = cursor_src.fetchall()

    # Lecture des données de la table relations
    cursor_src.execute('SELECT * FROM relations')
    relations_data = cursor_src.fetchall()

    # Calcul du nombre total de lignes à insérer
    total_lignes = len(parents_data) + len(relations_data)

    # chargement_meter2['amounttotal'] = len(parents_data) + len(relations_data)

    # Fonction interne pour insérer les données et mettre à jour le Meter progressivement
    def insert_data(i=0):
        # Mise à jour du Meter
        chargement_meter2['amountused'] = i
        if i < len(parents_data):
            # Insertion des données dans la table users
            parent = parents_data[i]
            cursor_src.execute(f'''
                INSERT INTO {nom_user} (
                    id, nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation,
                    montant, don, mode_paiement, membre_ca, recevoir_entre_nous, date_paiement, commentaire
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', parent)
        elif i < len(parents_data) + len(relations_data):
            chargement_meter2['subtext'] = "Copie des \n relation"
            # Insertion des données dans la table relations
            relation = relations_data[i - len(parents_data)]
            cursor_src.execute(f'''
                INSERT INTO {nom_relations} (parent_id, child_id) VALUES (?, ?)
            ''', relation)
        else:
            # Toutes les données ont été insérées
            conn_src.commit()
            conn_src.close()
            chargement_meter2.destroy()
            maj_menu_deroulent_table()
            return

        # Mise à jour du Meter
        chargement_meter2['amountused'] = int((i + 1) / total_lignes * 100)

        # Planifier la prochaine insertion
        root.after(5, insert_data, i + 1)

    # Commencer l'insertion des données
    insert_data()


def creat_new_table():
    
    nom_user = f"users{annee_en_cours}".replace("-", "_")
    nom_relations = f"relations{annee_en_cours}".replace("-", "_")
    
    # Connexion à la base de données de destination pour créer les tables
    conn = sqlite3.connect('association.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO name_table (user, relation) VALUES (?, ?)', (nom_user, nom_relations))

    #id_table = conn.lastrowid

    # Création de la table des utilisateurs
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {nom_user} (
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
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {nom_relations} (
        parent_id INTEGER,
        child_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES users(id),
        FOREIGN KEY (child_id) REFERENCES users(id)
    )
    ''')

    conn.commit()


    conn.close()

    return nom_user, nom_relations


def mise_a_jour_table():
    annee_dernier = int(annee_en_cours) - 1

    conn = sqlite3.connect('association.db')
    cursor = conn.cursor()
    # Sélectionner les utilisateurs dont la cotisation est égale à 2023
    cursor.execute(f'SELECT id FROM users WHERE cotisation = "{annee_dernier}"')
    utilisateurs_a_supprimer = cursor.fetchall()

    # Supprimer les relations associées à ces utilisateurs
    for utilisateur in utilisateurs_a_supprimer:
        utilisateur_id = utilisateur[0]
        cursor.execute('DELETE FROM relations WHERE parent_id = ? OR child_id = ?',
                       (utilisateur_id, utilisateur_id))

    # Supprimer les utilisateurs de la table users
    cursor.execute(f'DELETE FROM users WHERE cotisation = "{annee_dernier}"')
    # Valider les changements
    conn.commit()

    # Fermer la connexion à la base de données
    conn.close()

    mettre_a_jour_tableau()

    messagebox.showinfo("Confirmation", "Suppression anciens utilisateurs effectuée.")


# tester avec un signe si la valeur est compris
def age_tester(age_range_str, age_tester):
    age_tester = int(annee_en_cours) - int(age_tester)
    age_range_str = age_range_str.replace(" ", "")

    if '>=' in age_range_str:
        # Plus grand que
        try:
            if age_range_str.split('>=')[0] == "":
                age = int(age_range_str.split('>=')[1])
                return age_tester <= age
            else:
                age = int(age_range_str.split('>=')[0])
                return age_tester >= age

        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))

    elif '=>' in age_range_str:
        try:
            if age_range_str.split('=>')[0] == "":
                age = int(age_range_str.split('=>')[1])
                return age_tester <= age
            else:
                age = int(age_range_str.split('=>')[0])
                return age_tester >= age

        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    elif '>' in age_range_str:
        try:
            sense = age_range_str.split('>')[0]
            if sense == "":  # >15 plus petit
                age = int(age_range_str.split('>')[1])
                return age_tester < age
            else:  # 15> plus grand
                age = int(age_range_str.split('>')[0])
                return age_tester > age
        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))

    elif '<=' in age_range_str:
        try:
            if age_range_str.split('<=')[0] == "":
                age = int(age_range_str.split('<=')[1])
                return age_tester >= age
            else:
                age = int(age_range_str.split('<=')[0])
                return age_tester <= age

        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    elif '=<' in age_range_str:
        try:
            if age_range_str.split('=<')[0] == "":
                age = int(age_range_str.split('=<')[1])
                return age_tester >= age
            else:
                age = int(age_range_str.split('=<')[0])
                return age_tester <= age

        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    elif '<' in age_range_str:
        try:
            if age_range_str.split('<')[0] == "":
                age = int(age_range_str.split('<')[1])
                return age_tester > age
            else:
                age = int(age_range_str.split('<')[0])
                return age_tester < age

        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    elif '-' in age_range_str:
        # Entre deux âges
        try:
            age_min, age_max = map(int, age_range_str.split('-'))
            age_min = age_min
            age_max = age_max
            return age_min <= age_tester <= age_max
        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    else:
        try:
            return age_tester == int(age_range_str)
        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))


# Fonction pour charger les données depuis SQLite
def charger_donnees():
    global relation_table
    table_name = colonne_var_table.get()
    id_table = table_name[:1]

    conn = sqlite3.connect('association.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT user FROM name_table WHERE id = "{id_table}"')
    user_table = cursor.fetchall()

    cursor.execute(f'SELECT relation FROM name_table WHERE id = "{id_table}"')
    relation_table = cursor.fetchall()

    if user_table == []:
        user_table = "users"
        relation_table = "relations"
    else:
        user_table = user_table[0][0]
        relation_table = relation_table[0][0]

    cursor.execute(f'SELECT * FROM {user_table}')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_children(parent_id):
    conn = sqlite3.connect('association.db')
    c = conn.cursor()
    c.execute(f'''
    SELECT * FROM users
    JOIN {relation_table} ON users.id = {relation_table}.child_id
    WHERE {relation_table}.parent_id = ?
    ''', (parent_id,))
    conn.commit()
    enfant_get = c.fetchall()
    conn.close()
    return enfant_get

def get_parents(child_id):
    conn = sqlite3.connect('association.db')
    c = conn.cursor()

    c.execute('''
    SELECT users.id, users.name FROM users
    JOIN relations ON users.id = relations.parent_id
    WHERE relations.child_id = ?
    ''', (child_id,))
    conn.commit()
    parent_get = c.fetchall()
    conn.close()

    return parent_get

# Fonction pour mettre à jour le tableau avec les données
def mettre_a_jour_tableau(data=None):

    for row in tableau.get_children():
        tableau.delete(row)

    if data is None:
        data = charger_donnees()

    for i, row in enumerate(data, start=1):
        # Conversion du tuple en liste
        liste_temporaire = list(row)

        # Modification du 4ème élément
        if liste_temporaire[3] != "":
            liste_temporaire[3] = int(annee_en_cours) - int(liste_temporaire[3])
            # Conversion de la liste de retour en tuple
            row_2 = tuple(liste_temporaire)
        else:
            row_2 = row


        row_list = list(row_2)
        row_list[7] = str(row_list[7])  # Make sure phone number stays a string
        row2 = tuple(row_list)


        if i % 2 == 0:
            parent1 = tableau.insert('', 'end', values=row2, open=False, tags=('evenrow',))
        else:
            parent1 = tableau.insert('', 'end', values=row2, open=False, tags=('oddrow',))

        liste_enfant = get_children(row[0])
        for j, row_enfant in enumerate(liste_enfant):
            # Conversion du tuple en liste
            liste_temporaire = list(row_enfant)
            # Modification du 4ème élément (index 3, car les index commencent à 0)
            if liste_temporaire[3] != "":
                liste_temporaire[3] = int(annee_en_cours) - int(liste_temporaire[3])
                # Conversion de la liste de retour en tuple
                row_enfant2 = tuple(liste_temporaire)
            else:
                row_enfant2 = row_enfant


            if j % 2 == 0:
                tableau.insert(parent1, 'end', values=row_enfant2, tags=('evenrow2',))
            else:
                tableau.insert(parent1, 'end', values=row_enfant2, tags=('oddrow2',))

    longueur_label.config(text=f"Nombre élément: {get_treeview_length()}")




# Fonction de recherche
def rechercher(event=None):
    colonne = colonne_var.get()
    recherche = recherche_var.get()

    if not recherche:
        mettre_a_jour_tableau()
        return

    data = charger_donnees()
    resultats = []

    if colonne == "Tout":
        for row in data:
            for value in row:
                if recherche.lower() in str(value).lower():
                    resultats.append(row)
                    break
    elif colonne == "age":
        col_index = colonnes.index(colonne)
        for row in data:
            if row[col_index] != "":
                if age_tester(recherche, row[col_index]):
                    resultats.append(row)
    else:
        col_index = colonnes.index(colonne)
        print(col_index)
        for row in data:
            # print(f"{recherche.lower()} in {str(row[col_index]).lower()} = {recherche.lower() in str(row[col_index]).lower()}")
            if recherche.lower() in str(row[col_index]).lower():
                resultats.append(row)

    mettre_a_jour_tableau(resultats)

def uniquement_chiffres(chaine):
    for char in chaine:
        if not (char.isdigit() or char == '.'):
            return False
    return True

def uniquement_lettres(chaine):
    for c in chaine:
        if not (c.isalpha() or c.isspace()):
            return False
    return True

def est_adresse_email_valide(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

def test_possible(data):

    if not uniquement_lettres(data["nom"]):
        return False, "Le NOM doit contenir uniquement des lettres.", "error"

    if not uniquement_lettres(data["prenom"]):
        return False, "Le PRENOM doit contenir uniquement des lettres.", "error"

    if not uniquement_chiffres(data["age"]):
        return False, "La DATE DE NAISSANCE doit contenir uniquement des chiffres.", "error"
    elif len(data["age"]) != 4 and data["age"] != "":
        return False, f"La DATE DE NAISSANCE doit contenir 4 chiffres, {len(data["age"])} donné", "error"

    if not uniquement_chiffres(data["code_postal"]):
        return False, "Le CODE POSTAL doit contenir uniquement des chiffres.", "error"
    elif len(data["code_postal"]) != 5 and data["code_postal"] != "":
        return False, f"Le CODE POSTAL doit contenir 5 chiffres, {len(data["code_postal"])} donné", "error"

    if not uniquement_chiffres(data["telephone"]):
        return False, "Le numéro de TELEPHONE doit contenir uniquement des chiffres.", "error"
    elif len(data["telephone"]) != 10 and data["telephone"] != "":
        return False, f"Le numéro de TELEPHONE doit contenir 10 chiffres, {len(data["telephone"])} donné", "error"

    if data["mail"] != "":
        if not est_adresse_email_valide(data["mail"]):
            return False, f"Veuillez entrer une adresse mail valide ", "error"

    if not uniquement_chiffres(data["montant"]):
        return False, "Le MONTANT doit contenir uniquement des chiffres.", "error"

    if not uniquement_chiffres(data["don"]):
        return False, "Le DON doit contenir uniquement des chiffres.", "error"

    return True, "Voulez-vous ajouter cet utilisateur ?", "valide"

def message(data):
    possible, message, type_message = test_possible(data)
    if possible and type_message == "valide":
        if messagebox.askyesno("Confirmation", message):
            return True
        else:
            return False

    elif possible and type_message == "attention":
        if messagebox.askyesno(type_message, message):
            return True
        else:
            return False

    else:
        messagebox.showerror("Erreur", message)
        return False

id_parent = None
afficher_champ_pas_rempli = True
afficher_champ_pas_rempli2 = True
# Fonction pour soumettre le formulaire et ajouter un utilisateur
def submit_form():
    global id_parent, afficher_champ_pas_rempli
    data = {
        "nom": nom_entry.get().upper(),
        "prenom": prenom_entry.get().capitalize(),
        "age": age_entry.get().replace(" ", ""),
        "adresse": adresse_entry.get(),
        "code_postal": code_postal_entry.get().replace(" ", ""),
        "ville": ville_entry.get(),
        "telephone": telephone_entry.get().replace(" ", ""),
        "mail": mail_entry.get().replace(" ", ""),
        "type": type_combobox.get(),
        "activite": activite_combobox.get(),
        "cotisation": cotisation_entry.get().replace(" ", ""),
        "montant": montant_spinbox.get().replace(" ", ""),
        "don": don_spinbox.get().replace(" ", ""),
        "mode_paiement": mode_paiement_combobox.get(),
        "membre_ca": membre_ca_var.get(),
        "recevoir_entre_nous": entre_nous_var.get(),
        "date_paiement": date_DateEntry.entry.get(),
        "commentaire": commentaire_text.get("1.0", tk.END)
    }
    print(data["membre_ca"])
    if afficher_champ_pas_rempli:
        for key, value in data.items():
            if value == "":
                if not messagebox.askyesno("attention", "Tous les champs ne sont pas remplis, voulez-vous continuer ?"):
                    for key, value in child_windows.items():
                        child_windows[key]["window"].lift()
                    return None
                else:
                    afficher_champ_pas_rempli = False
                    break


    possible_end = message(data)
    if possible_end:
        afficher_champ_pas_rempli = True
        conn = sqlite3.connect('association.db')
        c = conn.cursor()
        c.execute('''
                            INSERT INTO users (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, date_paiement, membre_ca, recevoir_entre_nous, commentaire)
                            VALUES (:nom, :prenom, :age, :adresse, :code_postal, :ville, :telephone, :mail, :type, :activite, :cotisation, :montant, :don, :mode_paiement, :date_paiement, :membre_ca, :recevoir_entre_nous, :commentaire)
                        ''', data)
        conn.commit()

        id_parent = c.lastrowid

        conn.close()

        mettre_a_jour_tableau()
    for key, value in child_windows.items():
        child_windows[key]["window"].lift()


def insert_relation(parent_id, child_id):
    conn = sqlite3.connect('association.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO relations (parent_id, child_id) VALUES (?, ?)', (parent_id, child_id))
    conn.commit()
    conn.close()

def submit_form_enfant(key, parent_id):
    data = {
        "nom": child_windows[key]["nom_entry"].get(),
        "prenom": child_windows[key]["prenom_entry"].get(),
        "age": child_windows[key]["age_entry"].get(),
        "adresse": child_windows[key]["adresse_entry"].get(),
        "code_postal": child_windows[key]["code_postal_entry"].get(),
        "ville": child_windows[key]["ville_entry"].get(),
        "telephone": child_windows[key]["telephone_entry"].get(),
        "mail": child_windows[key]["mail_entry"].get(),
        "type": child_windows[key]["type_combobox"].get(),
        "activite": child_windows[key]["activite_combobox"].get(),
        "cotisation": child_windows[key]["cotisation_entry"].get(),
        "montant": child_windows[key]["montant_spinbox"].get(),
        "don": child_windows[key]["don_spinbox"].get(),
        "mode_paiement": child_windows[key]["mode_paiement_combobox"].get(),
        "membre_ca": child_windows[key]["membre_ca_var"].get(),
        "recevoir_entre_nous": child_windows[key]["entre_nous_var"].get(),
        "date_paiement": child_windows[key]["date_DateEntry"].entry.get(),
        "commentaire": child_windows[key]["commentaire_text"].get("1.0", tk.END)
    }

    for key2, value in data.items():
        if value == "":
            if not messagebox.askyesno("attention",
                                       "Tous les champs ne sont pas remplis, voulez-vous continuer ?"):
                for key, value in child_windows.items():
                    child_windows[key]["window"].lift()
                return None
            else:
                break

    possible_end = message(data)
    if possible_end:
        conn = sqlite3.connect('association.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, date_paiement, membre_ca, recevoir_entre_nous, commentaire)
            VALUES (:nom, :prenom, :age, :adresse, :code_postal, :ville, :telephone, :mail, :type, :activite, :cotisation, :montant, :don, :mode_paiement, :date_paiement, :membre_ca, :recevoir_entre_nous, :commentaire)
        ''', data)
        conn.commit()
        id_enfant = c.lastrowid
        conn.close()

        insert_relation(child_windows[key]["id_parent"].get(), id_enfant)

        mettre_a_jour_tableau()

        on_close(child_windows[key]["window"])

    for key, value in child_windows.items():
        child_windows[key]["window"].lift()

def creat_widget_modif():
    global nom_button, prenom_button, age_button, adresse_button, code_postal_button, ville_button, telephone_button, mail_button, cotisation_button, montant_spinbox, don_spinbox, mode_paiement_combobox, membre_ca_var, entre_nous_var, date_DateEntry, commentaire_text

    # Supprimer les anciens boutons
    for widget in tab3.winfo_children():
        widget.destroy()

    # Création des widgets pour le mode "copie"
    nom_label = ttk.Label(tab3, text="Nom")
    nom_button = ttk.Button(tab3, text="Nom", command=lambda: copy_to_clipboard("Nom"))

    prenom_label = ttk.Label(tab3, text="Prénom")
    prenom_button = ttk.Button(tab3, text="Prénom", command=lambda: copy_to_clipboard("Prénom"))

    age_label = ttk.Label(tab3, text="Année de naissance")
    age_button = ttk.Button(tab3, text="Année de naissance", command=lambda: copy_to_clipboard("Année de naissance"))

    adresse_label = ttk.Label(tab3, text="Adresse")
    adresse_button = ttk.Button(tab3, text="Adresse", command=lambda: copy_to_clipboard("Adresse"))

    code_postal_label = ttk.Label(tab3, text="Code postal")
    code_postal_button = ttk.Button(tab3, text="Code postal", command=lambda: copy_to_clipboard("Code postal"))

    ville_label = ttk.Label(tab3, text="Ville")
    ville_button = ttk.Button(tab3, text="Ville", command=lambda: copy_to_clipboard("Ville"))

    telephone_label = ttk.Label(tab3, text="Téléphone")
    telephone_button = ttk.Button(tab3, text="Téléphone", command=lambda: copy_to_clipboard("Téléphone"))

    mail_label = ttk.Label(tab3, text="Mail")
    mail_button = ttk.Button(tab3, text="Mail", command=lambda: copy_to_clipboard("Mail"))

    type_label = ttk.Label(tab3, text="Type")
    type_button = ttk.Button(tab3, text="Type", command=lambda: copy_to_clipboard("Type"))

    activite_label = ttk.Label(tab3, text="Activité")
    activite_button = ttk.Button(tab3, text="activité", command=lambda: copy_to_clipboard("activité"))

    cotisation_label = ttk.Label(tab3, text="Cotisation")
    cotisation_button = ttk.Button(tab3, text="Cotisation", command=lambda: copy_to_clipboard("Cotisation"))

    montant_label = ttk.Label(tab3, text="Montant")
    montant_button = ttk.Button(tab3, text="Montant", command=lambda: copy_to_clipboard("Montant"))

    don_label = ttk.Label(tab3, text="Don")
    don_button = ttk.Button(tab3, text="Don", command=lambda: copy_to_clipboard("Don"))

    mode_paiement_label = ttk.Label(tab3, text="Mode paiement")
    mode_paiement_button = ttk.Button(tab3, text="Mode paiement", command=lambda: copy_to_clipboard("Mode paiement"))

    date_label = ttk.Label(tab3, text="Date")
    date_button = ttk.Button(tab3, text="Date", command=lambda: copy_to_clipboard("Date"))

    commentaire_label = ttk.Label(tab3, text="Commentaire")
    commentaire_button = ttk.Button(tab3, text="Commentaire", command=lambda: copy_to_clipboard("Commentaire"))


    modify_button = ttk.Button(tab3, text="Modifier", command=switch_mode)

    # # Placement des widgets
    widgets_modif = [
        (nom_label, 0, 0), (nom_button, 0, 1),
        (prenom_label, 1, 0), (prenom_button, 1, 1),
        (age_label, 2, 0), (age_button, 2, 1),
        (adresse_label, 3, 0), (adresse_button, 3, 1),
        (code_postal_label, 4, 0), (code_postal_button, 4, 1),
        (ville_label, 5, 0), (ville_button, 5, 1),
        (telephone_label, 6, 0), (telephone_button, 6, 1),
        (mail_label, 7, 0), (mail_button, 7, 1),
        (type_label, 0, 2), (type_button, 0, 3),
        (activite_label, 1, 2), (activite_button, 1, 3),
        (cotisation_label, 2, 2), (cotisation_button, 2, 3),
        (montant_label, 3, 2), (montant_button, 3, 3),
        (don_label, 4, 2), (don_button, 4, 3),
        (mode_paiement_label, 5, 2), (mode_paiement_button, 5, 3),
        (date_label, 6, 2), (date_button, 6, 3),
        (commentaire_label, 8, 0), (commentaire_button, 8, 1, 1, 4),
        # (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
        (modify_button, 9, 3)
    ]

    for widget in widgets_modif:
        if len(widget) == 3:
            if widget[0] == modify_button:
                widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
            else:
                widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="ew")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="ew")

def remplir_formulaire(row):
    global nom_button, prenom_button, age_button, adresse_button, code_postal_button, ville_button, telephone_button, mail_button, cotisation_button, montant_spinbox, don_spinbox, mode_paiement_combobox, membre_ca_var, entre_nous_var, date_DateEntry, commentaire_text

    creat_widget_modif()

    # try:
    age = int(annee_en_cours) - int(row[3])
    nom_button.config(text=row[1], command=lambda: copy_to_clipboard(row[1]))
    prenom_button.config(text=row[2], command=lambda: copy_to_clipboard(row[2]))
    age_button.config(text=age, command=lambda: copy_to_clipboard(age))
    adresse_button.config(text=row[4], command=lambda: copy_to_clipboard(row[4]))
    code_postal_button.config(text=row[5], command=lambda: copy_to_clipboard(row[5]))
    ville_button.config(text=row[6], command=lambda: copy_to_clipboard(row[6]))
    telephone_button.config(text=row[7], command=lambda: copy_to_clipboard(row[7]))
    print("row 7 copie")
    print(row[7])
    mail_button.config(text=row[8], command=lambda: copy_to_clipboard(row[8]))
    type_combobox.set(row[9])
    activite_combobox.set(row[10])
    cotisation_button.config(text=row[11], command=lambda: copy_to_clipboard(row[11]))
    montant_spinbox.delete(0, tk.END)
    montant_spinbox.insert(0, row[12])
    don_spinbox.delete(0, tk.END)
    don_spinbox.insert(0, row[13])
    mode_paiement_combobox.set(row[14])
    date_DateEntry.entry.delete(0, tk.END)
    date_DateEntry.entry.insert(0, row[17])
    commentaire_text.delete("1.0", tk.END)
    commentaire_text.insert(tk.END, row[18])
    notebook.select(tab3)
    # except Exception:
    #     print("error !!!!!!!!!!!!!!!!!!!!!")

# Fonction pour remplir les widgets du formulaire de modification
def remplir_formulaire_entry(row):
    global nom_entry_modif, prenom_entry_modif, age_entry_modif, adresse_entry_modif
    global code_postal_entry_modif, ville_entry_modif, telephone_entry_modif, mail_entry_modif
    global type_combobox_modif, activite_combobox_modif, cotisation_entry_modif, montant_spinbox_modif
    global don_spinbox_modif, mode_paiement_combobox_modif, date_DateEntry_modif, commentaire_text_modif
    global membre_ca_var_modif, entre_nous_var_modif

    # Supprimer les anciens boutons
    for widget in tab3.winfo_children():
        widget.destroy()

    age_transform = int(annee_en_cours) - int(row[3])

    tel = str(row[7])

    # Création des widgets Entry pour la modification
    nom_label = ttk.Label(tab3, text="Nom")
    nom_entry_modif = ttk.Entry(tab3)
    nom_entry_modif.insert(0, row[1])

    prenom_label = ttk.Label(tab3, text="Prénom")
    prenom_entry_modif = ttk.Entry(tab3)
    prenom_entry_modif.insert(0, row[2])

    age_label = ttk.Label(tab3, text="Année de naissance")
    age_entry_modif = ttk.Entry(tab3)
    age_entry_modif.insert(0, age_transform)

    adresse_label = ttk.Label(tab3, text="Adresse")
    adresse_entry_modif = ttk.Entry(tab3)
    adresse_entry_modif.insert(0, row[4])

    code_postal_label = ttk.Label(tab3, text="Code postal")
    code_postal_entry_modif = ttk.Entry(tab3)
    code_postal_entry_modif.insert(0, row[5])

    ville_label = ttk.Label(tab3, text="Ville")
    ville_entry_modif = ttk.Entry(tab3)
    ville_entry_modif.insert(0, row[6])

    telephone_label = ttk.Label(tab3, text="Téléphone")
    telephone_entry_modif = ttk.Entry(tab3)
    telephone_entry_modif.insert(0, tel)
    print("tel édition")
    print(tel)

    mail_label = ttk.Label(tab3, text="Mail")
    mail_entry_modif = ttk.Entry(tab3)
    mail_entry_modif.insert(0, row[8])

    type_label = ttk.Label(tab3, text="Type")
    type_combobox_modif = ttk.Combobox(tab3, values=["AVT", "AF", "PRO", "ASS", "PA", "Bénévole", "PA AUT"])
    type_combobox_modif.set(row[9])

    activite_label = ttk.Label(tab3, text="Activité")
    activite_combobox_modif = ttk.Combobox(tab3, values=["Option 1", "Option 2"])
    activite_combobox_modif.set(row[10])

    cotisation_label = ttk.Label(tab3, text="Cotisation")
    cotisation_entry_modif = ttk.Entry(tab3)
    cotisation_entry_modif.insert(0, row[11])

    montant_label = ttk.Label(tab3, text="Montant")
    montant_spinbox_modif = ttk.Spinbox(tab3, from_=0, to=1000000000)
    montant_spinbox_modif.insert(0, row[12])

    don_label = ttk.Label(tab3, text="Don")
    don_spinbox_modif = ttk.Spinbox(tab3, from_=0, to=1000000000)
    don_spinbox_modif.insert(0, row[13])

    mode_paiement_label = ttk.Label(tab3, text="Mode paiement")
    mode_paiement_combobox_modif = ttk.Combobox(tab3, values=["Option 1", "Option 2"])
    mode_paiement_combobox_modif.set(row[14])

    date_label = ttk.Label(tab3, text="Date")
    # Convertir la chaîne de date en objet datetime.date
    startdate = datetime.strptime(row[17], '%Y-%m-%d').date()
    date_DateEntry_modif = ttk.DateEntry(tab3, dateformat='%Y-%m-%d', firstweekday=2, startdate=startdate)
    date_DateEntry_modif.entry.delete(0, tk.END)
    date_DateEntry_modif.entry.insert(0, row[17])

    commentaire_label = ttk.Label(tab3, text="Commentaire")
    commentaire_text_modif = tk.Text(tab3, height=5, width=40)
    commentaire_text_modif.insert(tk.END, row[18])

    membre_ca_var_modif = tk.BooleanVar(value=row[15])
    membre_ca_check_modif = ttk.Checkbutton(tab3, text="Membre CA", variable=membre_ca_var_modif)

    entre_nous_var_modif = tk.BooleanVar(value=row[16])
    entre_nous_check_modif = ttk.Checkbutton(tab3, text="Entre nous", variable=entre_nous_var_modif)

    modify_button = ttk.Button(tab3, text="Valider", command=switch_mode)

    # Placement des widgets de modification
    widgets_modif = [
        (nom_label, 0, 0), (nom_entry_modif, 0, 1),
        (prenom_label, 1, 0), (prenom_entry_modif, 1, 1),
        (age_label, 2, 0), (age_entry_modif, 2, 1),
        (adresse_label, 3, 0), (adresse_entry_modif, 3, 1),
        (code_postal_label, 4, 0), (code_postal_entry_modif, 4, 1),
        (ville_label, 5, 0), (ville_entry_modif, 5, 1),
        (telephone_label, 6, 0), (telephone_entry_modif, 6, 1),
        (mail_label, 7, 0), (mail_entry_modif, 7, 1),
        (type_label, 0, 2), (type_combobox_modif, 0, 3),
        (activite_label, 1, 2), (activite_combobox_modif, 1, 3),
        (cotisation_label, 2, 2), (cotisation_entry_modif, 2, 3),
        (montant_label, 3, 2), (montant_spinbox_modif, 3, 3),
        (don_label, 4, 2), (don_spinbox_modif, 4, 3),
        (mode_paiement_label, 5, 2), (mode_paiement_combobox_modif, 5, 3),
        (date_label, 6, 2), (date_DateEntry_modif, 6, 3),
        (commentaire_label, 8, 0), (commentaire_text_modif, 8, 1, 1, 4),
        (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
        (modify_button, 9, 3)
    ]

    for widget in widgets_modif:
        if len(widget) == 3:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")

    notebook.select(tab3)

row_global = None
id_modif = None
# Fonction de gestion du double-clic sur une ligne du tableau
def on_double_click(event):
    global id_modif, row_global
    selected_item = tableau.selection()[0]
    item = tableau.item(selected_item, 'values')

    # Ensure phone number is treated as a string
    phone_number = str(item[7])

    # Debug print to check the value
    print(f"Retrieved phone number: {phone_number}")


    remplir_formulaire(item)


def update_form():
    global afficher_champ_pas_rempli2, possible_end_modif

    print("récupérer data pour modif")
    data = {
        # Récupérer les valeurs entrées/modifiées par l'utilisateur
        "nom": nom_entry_modif.get(),
        "prenom": prenom_entry_modif.get(),
        "age": age_entry_modif.get(),
        "adresse": adresse_entry_modif.get(),
        "code_postal": code_postal_entry_modif.get(),
        "ville": ville_entry_modif.get(),
        "telephone": telephone_entry_modif.get(),
        "mail": mail_entry_modif.get(),
        "type": type_combobox_modif.get(),
        "activite": activite_combobox_modif.get(),
        "cotisation": cotisation_entry_modif.get(),
        "montant": montant_spinbox_modif.get(),
        "don": don_spinbox_modif.get(),
        "mode_paiement": mode_paiement_combobox_modif.get(),
        "date_paiement": date_DateEntry_modif.entry.get(),
        "membre_ca": membre_ca_var_modif.get(),
        "recevoir_entre_nous": entre_nous_var_modif.get(),
        "commentaire": commentaire_text_modif.get("1.0", "end-1c"),  # Récupérer le texte du widget Text
    }

    for key, value in data.items():
        print(f"{key} : {value}")

    def message_modif(data):
        possible, message, type_message = test_possible(data)
        if possible and type_message == "valide":
            if messagebox.askyesno("Confirmation", "Voulez-vous modifier cet utilisateur ?"):
                return True
            else:
                return False

        elif possible and type_message == "attention":
            if messagebox.askyesno(type_message, message):
                return True
            else:
                return False

        else:
            if messagebox.askretrycancel("Erreur", message):
                print(f"Réessayer = None    -----  donc rien faire")
                return None
            else:
                return False

    if afficher_champ_pas_rempli2:
        for key, value in data.items():
            if value == "":
                if not messagebox.askyesno("attention",
                                           "Tous les champs ne sont pas remplis, voulez-vous continuer ?"):
                    selected_item = tableau.selection()
                    if selected_item:
                        selected_item1 = selected_item[0]
                        item = tableau.item(selected_item1)
                    return None
                else:
                    afficher_champ_pas_rempli2 = False
                    break

    possible_end_modif = message_modif(data)
    if possible_end_modif == True:
        print("modif : oui")
        afficher_champ_pas_rempli2 = True
        conn = sqlite3.connect('association.db')
        c = conn.cursor()

        # Exécution de la requête UPDATE avec les variables récupérées
        c.execute(f'''
            UPDATE users SET
                nom = :nom,
                prenom = :prenom,
                age = :age,
                adresse = :adresse,
                code_postal = :code_postal,
                ville = :ville,
                telephone = :telephone,
                mail = :mail,
                type = :type,
                activite = :activite,
                cotisation = :cotisation,
                montant = :montant,
                don = :don,
                mode_paiement = :mode_paiement,
                date_paiement = :date_paiement,
                membre_ca = :membre_ca,
                recevoir_entre_nous = :recevoir_entre_nous,
                commentaire = :commentaire
            WHERE id = {id_modif};
        ''', data)

        # Validation de la transaction
        conn.commit()
        # Fermeture de la connexion
        conn.close()

        # Enfin, rafraîchir le tableau principal ou les données mises à jour
        mettre_a_jour_tableau()  # Vous devez avoir déjà une fonction comme celle-ci pour rafraîchir le tableau

        # Afficher un message de succès ou effectuer d'autres actions nécessaires après la mise à jour
        #messagebox.showinfo("Succès", "Les informations ont été mises à jour avec succès!")


        # Vous pouvez également mettre à jour l'interface graphique ici si nécessaire
        nom_entry_modif.delete(0, tk.END)
        prenom_entry_modif.delete(0, tk.END)
        age_entry_modif.delete(0, tk.END)
        adresse_entry_modif.delete(0, tk.END)
        code_postal_entry_modif.delete(0, tk.END)
        ville_entry_modif.delete(0, tk.END)
        telephone_entry_modif.delete(0, tk.END)
        mail_entry_modif.delete(0, tk.END)
        type_combobox_modif.delete(0, tk.END)
        activite_combobox_modif.delete(0, tk.END)
        cotisation_entry_modif.delete(0, tk.END)
        montant_spinbox_modif.delete(0, tk.END)
        don_spinbox_modif.delete(0, tk.END)
        mode_paiement_combobox_modif.delete(0, tk.END)
        date_DateEntry_modif.entry.delete(0, tk.END)
        commentaire_text_modif.delete("1.0", tk.END)  # Récupérer le texte du widget Text

        notebook.select(tab1)

    elif possible_end_modif == False:
        print("False")
        selected_item = tableau.selection()
        if selected_item:
            selected_item1 = selected_item[0]
            item = tableau.item(selected_item1)
            print(item["values"])
            remplir_formulaire(item["values"])
    else:
        print("None")


def on_tab_selected(event):
    selected_tab_index = event.widget.index(event.widget.select())
    tab2_index = event.widget.index(tab2)

    if selected_tab_index == tab2_index:
        for key, value in child_windows.items():
            child_windows[key]["window"].lift()
    else:
        for key, value in child_windows.items():
            child_windows[key]["window"].lower()

def get_id_parent():
    global id_parent
    selected_item = tableau.selection()
    if selected_item:
        selected_item1 = selected_item[0]
        item = tableau.item(selected_item1)
        id_parent = item['values'][0]
        messagebox.showinfo("Confirmation", f"L'identifiant {id_parent} à bien été sélectionné ")
    else:
        messagebox.showerror("Erreur", "Aucun identifiant sélectionnée")


def delete_user_by_id():
    selected_item = tableau.selection()

    if selected_item:
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de supprimer à jamais cet utilisateur ?"):
            for i in selected_item:
                item = tableau.item(i)
                id_user = item['values'][0]

                # Connexion à la base de données
                conn = sqlite3.connect('association.db')
                cursor = conn.cursor()

                # Suppression de l'utilisateur par son ID
                cursor.execute('DELETE FROM users WHERE id = ?', (id_user,))

                # Committer les changements
                conn.commit()

                # Vérifier si l'utilisateur a été supprimé
                cursor.execute('SELECT changes()')
                changes = cursor.fetchone()[0]

                # Fermer la connexion
                conn.close()

                mettre_a_jour_tableau()

                if changes == 0:
                    print(f"Aucun utilisateur trouvé avec l'ID {id_user}.")
                    messagebox.showerror("Erreur", "Une erreur c'est produite")
                else:
                    print(f"L'utilisateur avec l'ID {id_user} a été supprimé.")
                    messagebox.showinfo("Confirmation", f"L'Utilisateur {item["values"][1]} {item["values"][2]} à bien été supprimé ")
    else:
        messagebox.showerror("Erreur", "Aucun identifiant sélectionnée")

# Création de la fenêtre principale
root = ttk.Window(themename="vapor")
root.title("Gestion des Utilisateurs et Tableau")
root.state('zoomed')

# Création d'un Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

# Création des onglets
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab3.grid_columnconfigure(1, weight=1)
tab3.grid_columnconfigure(3, weight=1)
tab3.grid_columnconfigure(4, weight=14)


notebook.add(tab1, text="Tableau")
notebook.add(tab2, text="Ajouter Utilisateur")
notebook.add(tab3, text="Fiche Utilisateur")
notebook.add(tab4, text="Nouvelle cotisation")

# Associez l'événement <<NotebookTabChanged>> au Notebook
notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

# ---------------- Onglet Tableau ---------------- #

# Frame de recherche
frame_recherche = ttk.Frame(tab1)
frame_recherche.pack(padx=10, pady=10, fill=tk.X)

recherche_var = tk.StringVar()
colonne_var = tk.StringVar()
colonne_var_table = tk.StringVar()

entry_recherche = ttk.Entry(frame_recherche, textvariable=recherche_var, width=50)
entry_recherche.pack(side=tk.LEFT, padx=5)

btn_recherche = ttk.Button(frame_recherche, text="🔍", style="secondary.Toolbutton.TButton", command=rechercher)
btn_recherche.pack(side=tk.LEFT, padx=5)

colonnes = ["id", "nom", "prénom", "age", "adresse", "code postal", "ville", "telephone", "mail",
            "type", "activité", "cotisation", "montant", "don", "mode paiement", "date paiement", "membre ca",
            "recevoir entre nous", "commentaire"]

# Connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('association.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM name_table')
nom_table_data_list = cursor.fetchall()

def maj_menu_deroulent_table():
    list_user_table = [f"{value[0]}-{value[1][5:]}" for i, value in enumerate(nom_table_data_list)]
    nom_tables.configure(values=["users"] + list_user_table)


menu_colonnes = ttk.Combobox(frame_recherche, textvariable=colonne_var, values=colonnes + ["Tout"], state='readonly')
menu_colonnes.set("Tout")
menu_colonnes.pack(side=tk.LEFT, padx=5)

nom_tables = ttk.Combobox(frame_recherche, textvariable=colonne_var_table, values=[], state='readonly')
maj_menu_deroulent_table()
nom_tables.set("users")
nom_tables.pack(side=tk.LEFT, padx=5)

btn_maj = ttk.Button(frame_recherche, text="ID parent ", style="secondary.Toolbutton.TButton", command=get_id_parent)
btn_maj.pack(side=tk.LEFT, padx=7)

btn_maj = ttk.Button(frame_recherche, text="Supprimer", style="secondary.Toolbutton.TButton", command=delete_user_by_id)
btn_maj.pack(side=tk.LEFT, padx=7)


# Frame principale
frame_principal = ttk.Frame(tab1)
frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(frame_principal)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = ttk.Scrollbar(frame_principal, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

tableau = ttk.Treeview(frame_principal, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9",
                                                 "col10", "col11", "col12", "col13", "col14", "col15",
                                                 "col16", "col17", "col18", "col19"), show="tree headings",
                       yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

tableau.heading("col1", text="id")
tableau.heading("col2", text="nom")
tableau.heading("col3", text="prénom")
tableau.heading("col4", text="age")
tableau.heading("col5", text="adresse")
tableau.heading("col6", text="code postal")
tableau.heading("col7", text="ville")
tableau.heading("col8", text="telephone")
tableau.heading("col9", text="mail")
tableau.heading("col10", text="type")
tableau.heading("col11", text="activité")
tableau.heading("col12", text="cotisation")
tableau.heading("col13", text="montant")
tableau.heading("col14", text="don")
tableau.heading("col15", text="mode paiement")
tableau.heading("col16", text="membre ca")
tableau.heading("col17", text="recevoir_entre_nous")
tableau.heading("col18", text="date_paiement")
tableau.heading("col19", text="commentaire")

tableau.column("col1", width=100, anchor=tk.CENTER)
tableau.column("col2", width=100, anchor=tk.CENTER)
tableau.column("col3", width=100, anchor=tk.CENTER)
tableau.column("col4", width=40, anchor=tk.CENTER)
tableau.column("col5", width=150, anchor=tk.CENTER)
tableau.column("col6", width=150, anchor=tk.CENTER)
tableau.column("col7", width=150, anchor=tk.CENTER)
tableau.column("col8", width=150, anchor=tk.CENTER)
tableau.column("col9", width=150, anchor=tk.CENTER)
tableau.column("col10", width=150, anchor=tk.CENTER)
tableau.column("col11", width=150, anchor=tk.CENTER)
tableau.column("col12", width=150, anchor=tk.CENTER)
tableau.column("col13", width=150, anchor=tk.CENTER)
tableau.column("col14", width=150, anchor=tk.CENTER)
tableau.column("col15", width=150, anchor=tk.CENTER)
tableau.column("col16", width=150, anchor=tk.CENTER)
tableau.column("col17", width=150, anchor=tk.CENTER)
tableau.column("col18", width=150, anchor=tk.CENTER)
tableau.column("col19", width=500, anchor=tk.W)

tableau.tag_configure('evenrow', background='#330066')
tableau.tag_configure('oddrow', background='#4d0099')
tableau.tag_configure('evenrow2', background='#9a26d4')
tableau.tag_configure('oddrow2', background='#ae4ede')

style = Style(theme='vapor')
style.configure('Treeview', rowheight=40)  # Augmentez la valeur de rowheight pour une épaisseur de ligne plus grande
style.map('Treeview', background=[('selected', style.colors.secondary)], foreground=[('selected', 'white')])

# Création d'un label pour afficher la longueur du tableau
longueur_label = ttk.Label(frame_recherche, text=f"Nombre élément: {get_treeview_length()}")
longueur_label.pack(side=tk.RIGHT, padx=20)

mettre_a_jour_tableau()

scrollbar_y.config(command=tableau.yview)
scrollbar_x.config(command=tableau.xview)
tableau.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# btn_maj = ttk.Button(tab1, text="Mettre à jour le tableau", style="primary.Outline.TButton", command=mettre_a_jour_tableau)
# btn_maj.pack(pady=10)

# Fonction appelée lors du changement de valeur du combobox
def on_combobox_change(event):
    global combobox_timer
    if combobox_timer is not None:
        root.after_cancel(combobox_timer)
    combobox_timer = root.after(800, rechercher)

def on_combobox_change_table(event):
    global combobox_timer_table
    if combobox_timer_table is not None:
        root.after_cancel(combobox_timer_table)
    combobox_timer_table = root.after(800, rechercher)


# Associez l'événement de changement de valeur au combobox
combobox_timer = None
menu_colonnes.bind("<<ComboboxSelected>>", on_combobox_change)
combobox_timer_table = None
nom_tables.bind("<<ComboboxSelected>>", on_combobox_change_table)

tableau.bind("<Double-1>", on_double_click)
entry_recherche.bind("<KeyRelease>", rechercher)


# fonction ajouter utilisateur

ESPACEMENT_X = 20
ESPACEMENT_Y = 30

nomb_fenetre = 0
# Liste pour garder les références des fenêtres enfant
child_windows = {}

def open_new_window():
    global x_f_a, y_f_a, nomb_fenetre, child_windows
    new_window = tk.Toplevel(root)
    nomb_fenetre += 1
    new_window.title("Nouvelle fenêtre")
    # ---------------- Onglet Ajouter Utilisateur ---------------- #

    # Supprimer la référence de la liste lorsque la fenêtre est fermée
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_close(new_window))

    pos_x = 850
    pos_y = 0
    pos = None

    match nomb_fenetre % 3:
        case 1:
            pos_x = 850
            pos_y = 0
            pos = 1
        case 2:
            pos_x = 0
            pos_y = 500
            pos = 2
        case 0:
            pos_x = 850
            pos_y = 500
            pos = 3

    # x_f = pos_x + x_f_a
    # y_f = pos_y + y_f_a
    #
    # x_f = pos_x
    # y_f = pos_y

    x_f_a = 0
    y_f_a = 0

    x_test = 850
    y_test = 0

    peux_placer_end = False

    nomb_fenetre2 = 0

    while not peux_placer_end:

        for i in range(1, 4):
            nomb_fenetre2 += 1
            peux_placer = True
            match i:
                case 1:
                    x_test = 850
                    y_test = 0
                    pos = 1
                case 2:
                    x_test = 0
                    y_test = 500
                    pos = 2
                case 3:
                    x_test = 850
                    y_test = 500
                    pos = 3

            x_f = x_test + x_f_a
            y_f = y_test + y_f_a

            for key, value in child_windows.items():
                if x_f == child_windows[key]["x"] and y_f == child_windows[key]["y"]:
                    peux_placer = False

            if peux_placer:
                peux_placer_end = True
                break
        x_f_a += ESPACEMENT_X
        y_f_a += ESPACEMENT_Y

    membre_ca_var_child = tk.BooleanVar()
    entre_nous_var_child = tk.BooleanVar()

    # Ajouter la nouvelle fenêtre à la liste des fenêtres enfant
    child_windows[nomb_fenetre2] = {
        "window": new_window,
        "x": x_f,
        "y": y_f,
        "pos": pos,
        "nom_label": ttk.Label(new_window, text="Nom"),
        "nom_entry": ttk.Entry(new_window, width=30),

        "prenom_label": ttk.Label(new_window, text="Prénom"),
        "prenom_entry": ttk.Entry(new_window),

        "age_label": ttk.Label(new_window, text="Année de naissance"),
        "age_entry": ttk.Entry(new_window),

        "adresse_label": ttk.Label(new_window, text="Adresse"),
        "adresse_entry": ttk.Entry(new_window, width=30),

        "code_postal_label": ttk.Label(new_window, text="Code postal"),
        "code_postal_entry": ttk.Entry(new_window),

        "ville_label": ttk.Label(new_window, text="Ville"),
        "ville_entry": ttk.Entry(new_window),

        "telephone_label": ttk.Label(new_window, text="Téléphone"),
        "telephone_entry": ttk.Entry(new_window),

        "mail_label": ttk.Label(new_window, text="Mail"),
        "mail_entry": ttk.Entry(new_window),

        "type_label": ttk.Label(new_window, text="Type"),
        "type_combobox": ttk.Combobox(new_window, values=["Autiste", "Amis famille", "Prof", "Association", "Parent", "Bénévole", "Parent autiste", "Enfant"]),

        "activite_label": ttk.Label(new_window, text="Activité"),
        "activite_combobox": ttk.Combobox(new_window, values=["Music", "Café asperger ", "Théatre", "Chant", "GHS", "HS", "Café asperger ado"]),

        "cotisation_label": ttk.Label(new_window, text="Cotisation"),
        "cotisation_entry": ttk.Entry(new_window),

        "montant_label": ttk.Label(new_window, text="Montant"),
        "montant_spinbox": ttk.Spinbox(new_window, from_=0, to=1000000000000000000000000000000000),

        "don_label": ttk.Label(new_window, text="don"),
        "don_spinbox": ttk.Spinbox(new_window, from_=0, to=1000000000000000000000000000000000),

        "mode_paiement_label": ttk.Label(new_window, text="Mode paiement"),
        "mode_paiement_combobox": ttk.Combobox(tab2, values=["virement", "helloasso", "espèce", "cheque"]),

        "dt": datetime.now().date(),
        "date_label": ttk.Label(new_window, text="Date paiement"),
        "date_DateEntry": ttk.DateEntry(new_window, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY),

        "commentaire_label": ttk.Label(new_window, text="Commentaire"),
        "commentaire_text": tk.Text(new_window, height=5, width=40),

        "membre_ca_var": membre_ca_var_child,
        "membre_ca_check": ttk.Checkbutton(new_window, text="Membre CA", variable=membre_ca_var_child),

        "entre_nous_var": entre_nous_var_child,
        "entre_nous_check": ttk.Checkbutton(new_window, text="Entre nous", variable=entre_nous_var_child),

        "submit_button": ttk.Button(new_window, text="Valider", command=lambda:submit_form_enfant(nomb_fenetre2, id_parent)),

        "id_parent_label": ttk.Label(new_window, text="id du parent"),
        "id_parent": ttk.Entry(new_window),

        #"ajouter_enfant": ttk.Button(new_window, text="Ouvrir une nouvelle fenêtre", command=open_new_window),
    }
    if id_parent != None:
        child_windows[nomb_fenetre2]["id_parent"].insert(tk.END, id_parent)

    widgets = [
        (child_windows[nomb_fenetre2]["nom_label"], 0, 0), (child_windows[nomb_fenetre2]["nom_entry"], 0, 1),
        (child_windows[nomb_fenetre2]["prenom_label"], 1, 0), (child_windows[nomb_fenetre2]["prenom_entry"], 1, 1),
        (child_windows[nomb_fenetre2]["age_label"], 2, 0), (child_windows[nomb_fenetre2]["age_entry"], 2, 1),
        (child_windows[nomb_fenetre2]["adresse_label"], 3, 0), (child_windows[nomb_fenetre2]["adresse_entry"], 3, 1),
        (child_windows[nomb_fenetre2]["code_postal_label"], 4, 0), (child_windows[nomb_fenetre2]["code_postal_entry"], 4, 1),
        (child_windows[nomb_fenetre2]["ville_label"], 5, 0), (child_windows[nomb_fenetre2]["ville_entry"], 5, 1),
        (child_windows[nomb_fenetre2]["telephone_label"], 6, 0), (child_windows[nomb_fenetre2]["telephone_entry"], 6, 1),
        (child_windows[nomb_fenetre2]["mail_label"], 7, 0), (child_windows[nomb_fenetre2]["mail_entry"], 7, 1),
        (child_windows[nomb_fenetre2]["type_label"], 0, 2), (child_windows[nomb_fenetre2]["type_combobox"], 0, 3),
        (child_windows[nomb_fenetre2]["activite_label"], 1, 2), (child_windows[nomb_fenetre2]["activite_combobox"], 1, 3),
        (child_windows[nomb_fenetre2]["cotisation_label"], 2, 2), (child_windows[nomb_fenetre2]["cotisation_entry"], 2, 3),
        (child_windows[nomb_fenetre2]["montant_label"], 3, 2), (child_windows[nomb_fenetre2]["montant_spinbox"], 3, 3),
        (child_windows[nomb_fenetre2]["don_label"], 4, 2), (child_windows[nomb_fenetre2]["don_spinbox"], 4, 3),
        (child_windows[nomb_fenetre2]["mode_paiement_label"], 5, 2), (child_windows[nomb_fenetre2]["mode_paiement_combobox"], 5, 3),
        (child_windows[nomb_fenetre2]["date_label"], 6, 2), (child_windows[nomb_fenetre2]["date_DateEntry"], 6, 3),
        (child_windows[nomb_fenetre2]["commentaire_label"], 8, 0), (child_windows[nomb_fenetre2]["commentaire_text"], 8, 1, 1, 4),
        (child_windows[nomb_fenetre2]["membre_ca_check"], 7, 2), (child_windows[nomb_fenetre2]["entre_nous_check"], 7, 3),
        (child_windows[nomb_fenetre2]["id_parent_label"], 9, 2), (child_windows[nomb_fenetre2]["id_parent"], 9, 3),
        (child_windows[nomb_fenetre2]["submit_button"], 11, 2),


        #, (child_windows[nomb_fenetre2]["ajouter_enfant"], 9, 3)
    ]

    for widget in widgets:
        if len(widget) == 3:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="w")

    child_windows = dict(sorted(child_windows.items()))


    # Réinitialiser la taille et la position de la nouvelle fenêtre
    new_window.geometry(f"+{x_f}+{y_f}")

    pos_fnt_avant_plan = nomb_fenetre % 3

    for key, value in child_windows.items():
        child_windows[key]["window"].lift()




def on_close(window):
    keys_to_delete = []
    for key, value in child_windows.items():
        if window == value["window"]:
            keys_to_delete.append(key)
            value["window"].destroy()

    for key in keys_to_delete:
        child_windows.pop(key)

    for key, value in child_windows.items():
        child_windows[key]["window"].lift()


# ---------------- Onglet Ajouter Utilisateur ---------------- #

nom_label = ttk.Label(tab2, text="Nom")
nom_entry = ttk.Entry(tab2, width=30)

prenom_label = ttk.Label(tab2, text="Prénom")
prenom_entry = ttk.Entry(tab2)

age_label = ttk.Label(tab2, text="Année de naissance")
age_entry = ttk.Entry(tab2)

adresse_label = ttk.Label(tab2, text="Adresse")
adresse_entry = ttk.Entry(tab2, width=30)

code_postal_label = ttk.Label(tab2, text="Code postal")
code_postal_entry = ttk.Entry(tab2)

ville_label = ttk.Label(tab2, text="Ville")
ville_entry = ttk.Entry(tab2)

telephone_label = ttk.Label(tab2, text="Téléphone")
telephone_entry = ttk.Entry(tab2)

mail_label = ttk.Label(tab2, text="Mail")
mail_entry = ttk.Entry(tab2)

type_label = ttk.Label(tab2, text="Type")
type_combobox = ttk.Combobox(tab2, values=["Autiste", "Amis famille", "Prof", "Association", "Parent", "Bénévole", "Parent autiste", "Enfant"])

activite_label = ttk.Label(tab2, text="Activité")
activite_combobox = ttk.Combobox(tab2, values=["Music", "Café asperger ", "Théatre", "Chant", "GHS", "HS", "Café asperger ado"])



list_year = [str(i) for i in range(annee_en_cours  - 2, annee_en_cours  + 2)]

cotisation_label = ttk.Label(tab2, text="Cotisation")
cotisation_entry = ttk.Combobox(tab2, values=list_year)
cotisation_entry.insert(tk.END, annee_en_cours)

montant_label = ttk.Label(tab2, text="Montant")
montant_spinbox = ttk.Spinbox(tab2, from_=0, to=1000000000000000000000000000000000)

don_label = ttk.Label(tab2, text="don")
don_spinbox = ttk.Spinbox(tab2, from_=0, to=1000000000000000000000000000000000)

mode_paiement_label = ttk.Label(tab2, text="Mode paiement")
mode_paiement_combobox = ttk.Combobox(tab2, values=["virement", "helloasso", "espèce", "cheque"])

dt = datetime.now().date()
date_label = ttk.Label(tab2, text="Date paiement")
date_DateEntry = ttk.DateEntry(tab2, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY)

commentaire_label = ttk.Label(tab2, text="Commentaire")
commentaire_text = tk.Text(tab2, height=5, width=40)

membre_ca_var = tk.BooleanVar()
membre_ca_check = ttk.Checkbutton(tab2, text="Membre CA", variable=membre_ca_var)

entre_nous_var = tk.BooleanVar()
entre_nous_check = ttk.Checkbutton(tab2, text="Entre nous", variable=entre_nous_var)

submit_button = ttk.Button(tab2, text="Valider", command=submit_form)

ajouter_enfant = ttk.Button(tab2, text="ajouter un enfant", command=open_new_window)

widgets2 = [
    (nom_label, 0, 0), (nom_entry, 0, 1),
    (prenom_label, 1, 0), (prenom_entry, 1, 1),
    (age_label, 2, 0), (age_entry, 2, 1),
    (adresse_label, 3, 0), (adresse_entry, 3, 1),
    (code_postal_label, 4, 0), (code_postal_entry, 4, 1),
    (ville_label, 5, 0), (ville_entry, 5, 1),
    (telephone_label, 6, 0), (telephone_entry, 6, 1),
    (mail_label, 7, 0), (mail_entry, 7, 1),
    (type_label, 0, 2), (type_combobox, 0, 3),
    (activite_label, 1, 2), (activite_combobox, 1, 3),
    (cotisation_label, 2, 2), (cotisation_entry, 2, 3),
    (montant_label, 3, 2), (montant_spinbox, 3, 3),
    (don_label, 4, 2), (don_spinbox, 4, 3),
    (mode_paiement_label, 5, 2), (mode_paiement_combobox, 5, 3),
    (date_label, 6, 2), (date_DateEntry, 6, 3),
    (commentaire_label, 8, 0), (commentaire_text, 8, 1, 1, 4),
    (membre_ca_check, 7, 2), (entre_nous_check, 7, 3),
    (submit_button, 9, 2), (ajouter_enfant, 9, 3)
]

for widget in widgets2:
    if len(widget) == 3:
        widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")

# ---------------- Onglet Modifier Utilisateur ---------------- #

def copy_to_clipboard(text):
    pyperclip.copy(text)


# row_list = list(row_2)
# row_list[7] = str(row_list[7])  # Make sure phone number stays a string
# row2 = tuple(row_list)
def switch_mode():
    global edit_mode, id_modif
    if possible_end_modif == True or possible_end_modif == False:
        edit_mode = not edit_mode
    print(f"\n possible end modif = {possible_end_modif} | edite mode = {edit_mode} \n")
    if edit_mode:
        print("modifi")
        show_edit_widgets()
        selected_item = tableau.selection()[0]
        item = tableau.item(selected_item, 'values')

        # Assurez-vous que l'ID de l'élément sélectionné est défini
        id_modif = item[0]  # Supposons que l'ID soit le premier élément de 'values'

        remplir_formulaire_entry(item)
        #modify_button.config(text="Valider", command=update_form)
    else:
        print("valider")
        update_form()

        # creat_widget_modif()

def show_copy_widgets():
    # Création des widgets pour le mode "copie"
    nom_label = ttk.Label(tab3, text="Nom")
    nom_button = ttk.Button(tab3, text="Nom", command=lambda: copy_to_clipboard("Nom"))

    prenom_label = ttk.Label(tab3, text="Prénom")
    prenom_button = ttk.Button(tab3, text="Prénom", command=lambda: copy_to_clipboard("Prénom"))

    age_label = ttk.Label(tab3, text="Année de naissance")
    age_button = ttk.Button(tab3, text="Année de naissance", command=lambda: copy_to_clipboard("Année de naissance"))

    adresse_label = ttk.Label(tab3, text="Adresse")
    adresse_button = ttk.Button(tab3, text="Adresse", command=lambda: copy_to_clipboard("Adresse"))

    code_postal_label = ttk.Label(tab3, text="Code postal")
    code_postal_button = ttk.Button(tab3, text="Code postal", command=lambda: copy_to_clipboard("Code postal"))

    ville_label = ttk.Label(tab3, text="Ville")
    ville_button = ttk.Button(tab3, text="Ville", command=lambda: copy_to_clipboard("Ville"))

    telephone_label = ttk.Label(tab3, text="Téléphone")
    telephone_button = ttk.Button(tab3, text="Téléphone", command=lambda: copy_to_clipboard("Téléphone"))

    mail_label = ttk.Label(tab3, text="Mail")
    mail_button = ttk.Button(tab3, text="Mail", command=lambda: copy_to_clipboard("Mail"))

    type_label = ttk.Label(tab3, text="Type")
    type_button = ttk.Button(tab3, text="Type", command=lambda: copy_to_clipboard("Type"))

    activite_label = ttk.Label(tab3, text="Activité")
    activite_button = ttk.Button(tab3, text="activité", command=lambda: copy_to_clipboard("activité"))

    cotisation_label = ttk.Label(tab3, text="Cotisation")
    cotisation_button = ttk.Button(tab3, text="Cotisation", command=lambda: copy_to_clipboard("Cotisation"))

    montant_label = ttk.Label(tab3, text="Montant")
    montant_button = ttk.Button(tab3, text="Montant", command=lambda: copy_to_clipboard("Montant"))

    don_label = ttk.Label(tab3, text="Don")
    don_button = ttk.Button(tab3, text="Don", command=lambda: copy_to_clipboard("Don"))

    mode_paiement_label = ttk.Label(tab3, text="Mode paiement")
    mode_paiement_button = ttk.Button(tab3, text="Mode paiement", command=lambda: copy_to_clipboard("Mode paiement"))

    dt = datetime.now().date()
    date_label = ttk.Label(tab3, text="Date")
    date_DateEntry = ttk.DateEntry(dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY)

    commentaire_label = ttk.Label(tab3, text="Commentaire")
    commentaire_button = ttk.Button(tab3, text="Commentaire", command=lambda: copy_to_clipboard("Commentaire"))

    submit_button = ttk.Button(tab3, text="Valider", command=submit_form)

    modify_button = ttk.Button(tab3, text="Modifier", command=switch_mode)

    # # Placement des widgets
    #
    widgets_modif = [
        (nom_label, 0, 0), (nom_button, 0, 1),
        (prenom_label, 1, 0), (prenom_button, 1, 1),
        (age_label, 2, 0), (age_button, 2, 1),
        (adresse_label, 3, 0), (adresse_button, 3, 1),
        (code_postal_label, 4, 0), (code_postal_button, 4, 1),
        (ville_label, 5, 0), (ville_button, 5, 1),
        (telephone_label, 6, 0), (telephone_button, 6, 1),
        (mail_label, 7, 0), (mail_button, 7, 1),
        (type_label, 0, 2), (type_button, 0, 3),
        (activite_label, 1, 2), (activite_button, 1, 3),
        (cotisation_label, 2, 2), (cotisation_button, 2, 3),
        (montant_label, 3, 2), (montant_button, 3, 3),
        (don_label, 4, 2), (don_button, 4, 3),
        (mode_paiement_label, 5, 2), (mode_paiement_button, 5, 3),
        (date_label, 6, 2), (date_DateEntry_modif, 6, 3),
        (commentaire_label, 8, 0), (commentaire_button, 8, 1, 1, 4),
        (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
        (modify_button, 9, 3)
    ]

    for widget in widgets_modif:
        if len(widget) == 3:
            if widget[0] == modify_button:
                widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
            else:
                widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="ew")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="ew")


    try:
        nom_entry_modif.grid_remove()
        prenom_entry_modif.grid_remove()
        age_entry_modif.grid_remove()
        adresse_entry_modif.grid_remove()
        code_postal_entry_modif.grid_remove()
        ville_entry_modif.grid_remove()
        telephone_entry_modif.grid_remove()
        mail_entry_modif.grid_remove()
    except:
        print("error in copy widget")


def show_edit_widgets():
    try:
        nom_button.grid_remove()
        prenom_button.grid_remove()
        age_button.grid_remove()
        adresse_button.grid_remove()
        code_postal_button.grid_remove()
        ville_button.grid_remove()
        telephone_button.grid_remove()
        mail_button.grid_remove()
    except Exception:
        print("error in edit widget")
        creat_widget_modif()
        try:
            nom_button.grid_remove()
            prenom_button.grid_remove()
            age_button.grid_remove()
            adresse_button.grid_remove()
            code_postal_button.grid_remove()
            ville_button.grid_remove()
            telephone_button.grid_remove()
            mail_button.grid_remove()
            print("good")
        except Exception:
            print("error in edit widget 2")

# Variable pour suivre le mode actuel
edit_mode = False

# Création des widgets pour le mode "copie"
nom_label = ttk.Label(tab3, text="Nom")
nom_button = ttk.Button(tab3, text="Nom", command=lambda: copy_to_clipboard("Nom"))

prenom_label = ttk.Label(tab3, text="Prénom")
prenom_button = ttk.Button(tab3, text="Prénom", command=lambda: copy_to_clipboard("Prénom"))

age_label = ttk.Label(tab3, text="Année de naissance")
age_button = ttk.Button(tab3, text="Année de naissance", command=lambda: copy_to_clipboard("Année de naissance"))

adresse_label = ttk.Label(tab3, text="Adresse")
adresse_button = ttk.Button(tab3, text="Adresse", command=lambda: copy_to_clipboard("Adresse"))

code_postal_label = ttk.Label(tab3, text="Code postal")
code_postal_button = ttk.Button(tab3, text="Code postal", command=lambda: copy_to_clipboard("Code postal"))

ville_label = ttk.Label(tab3, text="Ville")
ville_button = ttk.Button(tab3, text="Ville", command=lambda: copy_to_clipboard("Ville"))

telephone_label = ttk.Label(tab3, text="Téléphone")
telephone_button = ttk.Button(tab3, text="Téléphone", command=lambda: copy_to_clipboard("Téléphone"))

mail_label = ttk.Label(tab3, text="Mail")
mail_button = ttk.Button(tab3, text="Mail", command=lambda: copy_to_clipboard("Mail"))

type_label = ttk.Label(tab3, text="Type")
type_button = ttk.Button(tab3, text="Type", command=lambda: copy_to_clipboard("Type"))

activite_label = ttk.Label(tab3, text="Activité")
activite_button = ttk.Button(tab3, text="activité", command=lambda: copy_to_clipboard("activité"))

cotisation_label = ttk.Label(tab3, text="Cotisation")
cotisation_button = ttk.Button(tab3, text="Cotisation", command=lambda: copy_to_clipboard("Cotisation"))

montant_label = ttk.Label(tab3, text="Montant")
montant_button = ttk.Button(tab3, text="Montant", command=lambda: copy_to_clipboard("Montant"))

don_label = ttk.Label(tab3, text="Don")
don_button = ttk.Button(tab3, text="Don", command=lambda: copy_to_clipboard("Don"))

mode_paiement_label = ttk.Label(tab3, text="Mode paiement")
mode_paiement_button = ttk.Button(tab3, text="Mode paiement", command=lambda: copy_to_clipboard("Mode paiement"))


date_label = ttk.Label(tab3, text="Date")
date_button= ttk.Button(tab3, text="Date", command=lambda: copy_to_clipboard("Date"))

# dt = datetime.now().date()
# date_label = ttk.Label(tab3, text="Date")
# date_DateEntry = ttk.DateEntry(tab3, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY)


commentaire_label = ttk.Label(tab3, text="Commentaire")
commentaire_button = ttk.Button(tab3, text="Commentaire", command=lambda: copy_to_clipboard("Commentaire"))


submit_button = ttk.Button(tab3, text="Valider", command=submit_form)

modify_button = ttk.Button(tab3, text="Modifier", command=switch_mode)




# ********** Création des widgets pour le mode "édition" **********

nom_label_modif = ttk.Label(tab3, text="Nom")
nom_entry_modif = ttk.Entry(tab3)

prenom_label_modif = ttk.Label(tab3, text="Prénom")
prenom_entry_modif = ttk.Entry(tab3)

age_label_modif = ttk.Label(tab3, text="Année de naissance")
age_entry_modif = ttk.Entry(tab3)

adresse_label_modif = ttk.Label(tab3, text="Adresse")
adresse_entry_modif = ttk.Entry(tab3)

code_postal_label_modif = ttk.Label(tab3, text="Code postal")
code_postal_entry_modif = ttk.Entry(tab3)

ville_label_modif = ttk.Label(tab3, text="Ville")
ville_entry_modif = ttk.Entry(tab3)

telephone_label_modif = ttk.Label(tab3, text="Téléphone")
telephone_entry_modif = ttk.Entry(tab3)

mail_label_modif = ttk.Label(tab3, text="Mail")
mail_entry_modif = ttk.Entry(tab3)

type_label_modif = ttk.Label(tab3, text="Type")
type_combobox_modif = ttk.Combobox(tab3, values=["AVT", "AF", "PRO", "ASS", "PA", "Bénévole", "PA AUT"])

activite_label_modif = ttk.Label(tab3, text="Activité")
activite_combobox_modif = ttk.Combobox(tab3, values=["Option 1", "Option 2"])

cotisation_label_modif = ttk.Label(tab3, text="Cotisation")
cotisation_entry_modif = ttk.Entry(tab3)

montant_label_modif = ttk.Label(tab3, text="Montant")
montant_spinbox_modif = ttk.Spinbox(tab3, from_=0, to=1000000000000000000000000000000000)

don_label_modif = ttk.Label(tab3, text="don")
don_spinbox_modif = ttk.Spinbox(tab3, from_=0, to=1000000000000000000000000000000000)

mode_paiement_label_modif = ttk.Label(tab3, text="Mode paiement")
mode_paiement_combobox_modif = ttk.Combobox(tab3, values=["Option 1", "Option 2"])

date_label_modif = ttk.Label(tab3, text="Date paiement")
date_DateEntry_modif = ttk.DateEntry(tab3, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY)

commentaire_label_modif = ttk.Label(tab3, text="Commentaire")
commentaire_text_modif = tk.Text(tab3, height=5, width=40)

membre_ca_var_modif = tk.BooleanVar()
membre_ca_check_modif = ttk.Checkbutton(tab3, text="Membre CA", variable=membre_ca_var_modif)

entre_nous_var_modif = tk.BooleanVar()
entre_nous_check_modif = ttk.Checkbutton(tab3, text="Entre nous", variable=entre_nous_var_modif)

submit_button_modif = ttk.Button(tab3, text="Valider", command=update_form)

modify_button_modif = ttk.Button(tab3, text="Modifier", command=switch_mode)


# # Placement des widgets
widgets_modif = [
    (nom_label, 0, 0), (nom_button, 0, 1),
    (prenom_label, 1, 0), (prenom_button, 1, 1),
    (age_label, 2, 0), (age_button, 2, 1),
    (adresse_label, 3, 0), (adresse_button, 3, 1),
    (code_postal_label, 4, 0), (code_postal_button, 4, 1),
    (ville_label, 5, 0), (ville_button, 5, 1),
    (telephone_label, 6, 0), (telephone_button, 6, 1),
    (mail_label, 7, 0), (mail_button, 7, 1),
    (type_label, 0, 2), (type_button, 0, 3),
    (activite_label, 1, 2), (activite_button, 1, 3),
    (cotisation_label, 2, 2), (cotisation_button, 2, 3),
    (montant_label, 3, 2), (montant_button, 3, 3),
    (don_label, 4, 2), (don_button, 4, 3),
    (mode_paiement_label, 5, 2), (mode_paiement_button, 5, 3),
    (date_label, 6, 2), (date_button, 6, 3),
    (commentaire_label, 8, 0), (commentaire_button, 8, 1, 1, 4),
    # (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
    (modify_button, 9, 3)
]

for widget in widgets_modif:
    if len(widget) == 3:
        if widget[0] == modify_button:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        else:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="ew")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="ew")



# def test():
#     for i in range(101):
#         chargement_meter.configure(amountused=i)

# widget cotisation :
btn_maj = ttk.Button(tab4, text="Nouvelle cotisation", style="secondary.Toolbutton.TButton", command=copy_data)
btn_maj.place(x=20, y=20)

btn_del = ttk.Button(tab4, text="Supprimer anciens membres", style="secondary.Toolbutton.TButton", command=mise_a_jour_table)
btn_del.place(x=200, y=20)


# chargement_meter = ttk.Meter(tab4,bootstyle="success", amountused=0, metersize=200, interactive=True, stripethickness=2, meterthickness=100, textright="%")
# chargement_meter.place(x=80, y=80)


# chargement_meter3 = ttk.Meter(tab4, bootstyle="success", amountused=0, metersize=200, interactive=True,
#                                   stripethickness=2, meterthickness=15, subtext="nombre utilisateur\ncopié")
# chargement_meter3.place(x=500, y=180)
#
# for i in range(200):
#     chargement_meter2.configure(amountused=(i + 1) / 200 * 100)
#     print(f"{(i + 1) / 200 * 100}%")



# Lancement de la boucle principale
root.mainloop()

