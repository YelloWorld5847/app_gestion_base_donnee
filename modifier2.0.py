import tkinter as tk
import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from datetime import datetime
import pyperclip
from tkinter import messagebox

# tester avec un signe si la valeur est compris
def age_tester(age_range_str, age_tester):
    """Parse l'expression de tranche d'âge."""
    age_range_str = age_range_str.replace(" ","")

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
            return age_min <= age_tester <= age_max
        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))
    else:
        try:
            return age_tester > int(age_range_str)
        except ValueError:
            raise ValueError("Tranche d'âge invalide : {}".format(age_range_str))


# Fonction pour charger les données depuis SQLite
def charger_donnees():
    conn = sqlite3.connect('association.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parents')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fonction pour mettre à jour le tableau avec les données
def mettre_a_jour_tableau(data=None):
    for row in tableau.get_children():
        tableau.delete(row)

    if data is None:
        data = charger_donnees()

    for i, row in enumerate(data, start=1):
        if i % 2 == 0:
            tableau.insert('', 'end', values=row, tags=('evenrow',))
        else:
            tableau.insert('', 'end', values=row, tags=('oddrow',))

# Fonction de recherche
def rechercher():
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
        for row in data:
            if recherche.lower() in str(row[col_index]).lower():
                resultats.append(row)

    mettre_a_jour_tableau(resultats)

# Fonction pour soumettre le formulaire et ajouter un utilisateur
def submit_form():
    data = {
        "nom": nom_entry.get(),
        "prenom": prenom_entry.get(),
        "age": age_entry.get(),
        "adresse": adresse_entry.get(),
        "code_postal": code_postal_entry.get(),
        "ville": ville_entry.get(),
        "telephone": telephone_entry.get(),
        "mail": mail_entry.get(),
        "type": type_combobox.get(),
        "activite": activite_combobox.get(),
        "cotisation": cotisation_entry.get(),
        "montant": montant_spinbox.get(),
        "don": don_spinbox.get(),
        "mode_paiement": mode_paiement_combobox.get(),
        "membre_ca": membre_ca_var.get(),
        "recevoir_entre_nous": entre_nous_var.get(),
        "date_paiement": date_DateEntry.entry.get(),
        "commentaire": commentaire_text.get("1.0", tk.END)
    }

    conn = sqlite3.connect('association.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO parents (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, date_paiement, membre_ca, recevoir_entre_nous, commentaire)
        VALUES (:nom, :prenom, :age, :adresse, :code_postal, :ville, :telephone, :mail, :type, :activite, :cotisation, :montant, :don, :mode_paiement, :date_paiement, :membre_ca, :recevoir_entre_nous, :commentaire)
    ''', data)
    conn.commit()
    conn.close()

    mettre_a_jour_tableau()

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

    age_label = ttk.Label(tab3, text="Age")
    age_button = ttk.Button(tab3, text="Age", command=lambda: copy_to_clipboard("Age"))

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

    membre_ca_var = tk.BooleanVar()
    commentaire_button = ttk.Button(tab3, text="Membre CA", command=lambda: copy_to_clipboard("Membre CA"))

    entre_nous_var = tk.BooleanVar()
    entre_nous_check = ttk.Checkbutton(tab3, text="Entre nous", variable=entre_nous_var)

    submit_button = ttk.Button(tab3, text="Valider", command=submit_form)

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
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="w")

def remplir_formulaire(row):
    global nom_button, prenom_button, age_button, adresse_button, code_postal_button, ville_button, telephone_button, mail_button, cotisation_button, montant_spinbox, don_spinbox, mode_paiement_combobox, membre_ca_var, entre_nous_var, date_DateEntry, commentaire_text


    try:
        nom_button.config(text=row[1], command=lambda: copy_to_clipboard(row[1]))
        prenom_button.config(text=row[2], command=lambda: copy_to_clipboard(row[2]))
        age_button.config(text=row[3], command=lambda: copy_to_clipboard(row[3]))
        adresse_button.config(text=row[4], command=lambda: copy_to_clipboard(row[4]))
        code_postal_button.config(text=row[5], command=lambda: copy_to_clipboard(row[5]))
        ville_button.config(text=row[6], command=lambda: copy_to_clipboard(row[6]))
        telephone_button.config(text=row[7], command=lambda: copy_to_clipboard(row[7]))
        mail_button.config(text=row[8], command=lambda: copy_to_clipboard(row[8]))
        type_combobox.set(row[9])
        activite_combobox.set(row[10])
        cotisation_button.config(text=row[11], command=lambda: copy_to_clipboard(row[11]))
        montant_spinbox.delete(0, tk.END)
        montant_spinbox.insert(0, row[12])
        don_spinbox.delete(0, tk.END)
        don_spinbox.insert(0, row[13])
        mode_paiement_combobox.set(row[14])
        membre_ca_var.set(row[15])
        entre_nous_var.set(row[16])
        date_DateEntry.entry.delete(0, tk.END)
        date_DateEntry.entry.insert(0, row[17])
        commentaire_text.delete("1.0", tk.END)
        commentaire_text.insert(tk.END, row[18])
        notebook.select(tab3)
    except Exception:
        print("error !!!!!!!!!!!!!!!!!!!!!")

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

    # Création des widgets Entry pour la modification
    nom_label = ttk.Label(tab3, text="Nom")
    nom_entry_modif = ttk.Entry(tab3)
    nom_entry_modif.insert(0, row[1])

    prenom_label = ttk.Label(tab3, text="Prénom")
    prenom_entry_modif = ttk.Entry(tab3)
    prenom_entry_modif.insert(0, row[2])

    age_label = ttk.Label(tab3, text="Age")
    age_entry_modif = ttk.Entry(tab3)
    age_entry_modif.insert(0, row[3])

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
    telephone_entry_modif.insert(0, row[7])

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
    selected_item = tableau.selection()
    if selected_item:
        item = tableau.item(selected_item)
        id_modif = item['values'][0]
        print(id_modif)
        row_global = item['values']
        remplir_formulaire(item['values'])


def update_form():
    # Récupérer les valeurs entrées/modifiées par l'utilisateur
    nom = nom_entry_modif.get()
    prenom = prenom_entry_modif.get()
    age = age_entry_modif.get()
    adresse = adresse_entry_modif.get()
    code_postal = code_postal_entry_modif.get()
    ville = ville_entry_modif.get()
    telephone = telephone_entry_modif.get()
    mail = mail_entry_modif.get()
    type = type_combobox_modif.get()
    activite = activite_combobox_modif.get()
    cotisation = cotisation_entry_modif.get()
    montant = montant_spinbox_modif.get()
    don = don_spinbox_modif.get()
    mode_paiement = mode_paiement_combobox_modif.get()
    date_paiement = date_DateEntry_modif.entry.get()
    commentaire = commentaire_text_modif.get("1.0", "end-1c")  # Récupérer le texte du widget Text

    # Convertir les valeurs selon les besoins (par exemple, convertir en int ou float si nécessaire)

    # Effectuer la mise à jour dans votre base de données ou structure de données
    # Par exemple, ici, nous pourrions simplement imprimer les valeurs mises à jour
    print(f"Nom: {nom}")
    print(f"Prénom: {prenom}")
    print(f"Age: {age}")
    print(f"Adresse: {adresse}")
    print(f"Code postal: {code_postal}")
    print(f"Ville: {ville}")
    print(f"Téléphone: {telephone}")
    print(f"Mail: {mail}")
    print(f"Type: {type}")
    print(f"Activité: {activite}")
    print(f"Cotisation: {cotisation}")
    print(f"Montant: {montant}")
    print(f"Don: {don}")
    print(f"Mode de paiement: {mode_paiement}")
    print(f"Date de paiement: {date_paiement}")
    print(f"Commentaire: {commentaire}")

    conn = sqlite3.connect('association.db')
    c = conn.cursor()

    # Exécution de la requête UPDATE avec les variables récupérées
    c.execute(f'''
        UPDATE parents SET
            nom = ?,
            prenom = ?,
            age = ?,
            adresse = ?,
            code_postal = ?,
            ville = ?,
            telephone = ?,
            mail = ?,
            type = ?,
            activite = ?,
            cotisation = ?,
            montant = ?,
            don = ?,
            mode_paiement = ?,
            date_paiement = ?,
            commentaire = ?
        WHERE parent_id = {id_modif}
    ''', (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type,
          activite, cotisation, montant, don, mode_paiement, date_paiement, commentaire))

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
notebook.add(tab1, text="Tableau")
notebook.add(tab2, text="Ajouter Utilisateur")
notebook.add(tab3, text="Modifier Utilisateur")

# ---------------- Onglet Tableau ---------------- #
# Frame de recherche
frame_recherche = ttk.Frame(tab1)
frame_recherche.pack(padx=10, pady=10, fill=tk.X)

recherche_var = tk.StringVar()
colonne_var = tk.StringVar()

entry_recherche = ttk.Entry(frame_recherche, textvariable=recherche_var, width=50)
entry_recherche.pack(side=tk.LEFT, padx=5)

btn_recherche = ttk.Button(frame_recherche, text="🔍", style="secondary.Toolbutton.TButton", command=rechercher)
btn_recherche.pack(side=tk.LEFT, padx=5)

colonnes = ["id", "nom", "prénom", "age", "adresse", "code postal", "ville", "telephone", "mail",
            "type", "activité", "cotisation", "montant", "don", "mode paiement", "date paiement", "membre ca",
            "recevoir entre nous", "commentaire"]

c = ""
for i in colonnes:
    c += i + ", "
print(f"\n {c} \n")


menu_colonnes = ttk.Combobox(frame_recherche, textvariable=colonne_var, values=["Tout"] + colonnes, state='readonly')
menu_colonnes.set("Tout")
menu_colonnes.pack(side=tk.LEFT, padx=5)

# Frame principale
frame_principal = ttk.Frame(tab1)
frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(frame_principal)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = ttk.Scrollbar(frame_principal, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

tableau = ttk.Treeview(frame_principal, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9",
                                                 "col10", "col11", "col12", "col13", "col14", "col15",
                                                 "col16", "col17", "col18", "col19"), show="headings",
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

style = Style(theme='vapor')
style.configure('Treeview', rowheight=40)  # Augmentez la valeur de rowheight pour une épaisseur de ligne plus grande
style.map('Treeview', background=[('selected', style.colors.secondary)], foreground=[('selected', 'white')])

mettre_a_jour_tableau()

scrollbar_y.config(command=tableau.yview)
scrollbar_x.config(command=tableau.xview)
tableau.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

btn_maj = ttk.Button(frame_principal, text="Mettre à jour le tableau", style="primary.Outline.TButton", command=mettre_a_jour_tableau)
btn_maj.pack(pady=10)

tableau.bind("<Double-1>", on_double_click)

# ---------------- Onglet Ajouter Utilisateur ---------------- #
nom_label = ttk.Label(tab2, text="Nom")
nom_entry = ttk.Entry(tab2, width=30)

prenom_label = ttk.Label(tab2, text="Prénom")
prenom_entry = ttk.Entry(tab2)

age_label = ttk.Label(tab2, text="Age")
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
type_combobox = ttk.Combobox(tab2, values=["AVT", "AF", "PRO", "ASS", "PA", "Bénévole", "PA AUT"])

activite_label = ttk.Label(tab2, text="Activité")
activite_combobox = ttk.Combobox(tab2, values=["Option 1", "Option 2"])

cotisation_label = ttk.Label(tab2, text="Cotisation")
cotisation_entry = ttk.Entry(tab2)

montant_label = ttk.Label(tab2, text="Montant")
montant_spinbox = ttk.Spinbox(tab2, from_=0, to=1000000000000000000000000000000000)

don_label = ttk.Label(tab2, text="don")
don_spinbox = ttk.Spinbox(tab2, from_=0, to=1000000000000000000000000000000000)

mode_paiement_label = ttk.Label(tab2, text="Mode paiement")
mode_paiement_combobox = ttk.Combobox(tab2, values=["Option 1", "Option 2"])

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

widgets = [
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
    (submit_button, 9, 3)
]

for widget in widgets:
    if len(widget) == 3:
        widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")

# ---------------- Onglet Modifier Utilisateur ---------------- #

def copy_to_clipboard(text):
    pyperclip.copy(text)

# def submit_form():
#     data = {
#         "nom": nom_entry.get(),
#         "prenom": prenom_entry.get(),
#         "age": age_entry.get(),
#         "adresse": adresse_entry.get(),
#         "code_postal": code_postal_entry.get(),
#         "ville": ville_entry.get(),
#         "telephone": telephone_entry.get(),
#         "mail": mail_entry.get(),
#         "type": type_combobox.get(),
#         "activite": activite_combobox.get(),
#         "cotisation": cotisation_entry.get(),
#         "montant": montant_spinbox.get(),
#         "don": don_spinbox.get(),
#         "mode_paiement": mode_paiement_combobox.get(),
#         "date_paiement": date_DateEntry.entry.get(),
#         "commentaire": commentaire_text.get("1.0", tk.END),
#         "membre_ca": membre_ca_var.get(),
#         "recevoir_entre_nous": entre_nous_var.get()
#     }
#
#     conn = sqlite3.connect('association.db')
#     c = conn.cursor()
#     c.execute('''
#         INSERT INTO parents (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, date_paiement, commentaire, membre_ca, recevoir_entre_nous)
#         VALUES (:nom, :prenom, :age, :adresse, :code_postal, :ville, :telephone, :mail, :type, :activite, :cotisation, :montant, :don, :mode_paiement, :date_paiement, :commentaire, :membre_ca, :recevoir_entre_nous)
#     ''', data)
#     conn.commit()
#     conn.close()

def switch_mode():
    global edit_mode
    edit_mode = not edit_mode
    if edit_mode:
        print("entry widget")
        show_edit_widgets()
        selected_item = tableau.selection()
        if selected_item:
            item = tableau.item(selected_item)
            id_modif = item['values'][0]
            print(id_modif)

            remplir_formulaire_entry(item['values'])
        #modify_button.config(text="Valider", command=update_form)
    else:
        print("copie widget (bouton sur valider essaie => modifier")
        update_form()

        creat_widget_modif()
        #modify_button.config(text="Modifier", command=switch_mode)
        print("row global :", row_global)
        # if row_global != None:
        #     print("not None")
        #     remplir_formulaire(row_global) #show_copy_widgets()
        # else:
        print("None")

def show_copy_widgets():
    # nom_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    # prenom_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    # age_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    # adresse_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    # code_postal_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    # ville_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    # telephone_button.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    # mail_button.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    # Création des widgets pour le mode "copie"
    nom_label = ttk.Label(tab3, text="Nom")
    nom_button = ttk.Button(tab3, text="Nom", command=lambda: copy_to_clipboard("Nom"))

    prenom_label = ttk.Label(tab3, text="Prénom")
    prenom_button = ttk.Button(tab3, text="Prénom", command=lambda: copy_to_clipboard("Prénom"))

    age_label = ttk.Label(tab3, text="Age")
    age_button = ttk.Button(tab3, text="Age", command=lambda: copy_to_clipboard("Age"))

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

    membre_ca_var = tk.BooleanVar()
    membre_ca_check = ttk.Checkbutton(tab3, text="Membre CA", variable=membre_ca_var)

    entre_nous_var = tk.BooleanVar()
    entre_nous_check = ttk.Checkbutton(tab3, text="Entre nous", variable=entre_nous_var)

    submit_button = ttk.Button(tab3, text="Valider", command=submit_form)

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
        (date_label, 6, 2), (date_DateEntry_modif, 6, 3),
        (commentaire_label, 8, 0), (commentaire_button, 8, 1, 1, 4),
        (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
        (modify_button, 9, 3)
    ]

    for widget in widgets_modif:
        if len(widget) == 3:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="w")


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
    except:
        print("error in entry widget ")

    # nom_entry_modif.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    # prenom_entry_modif.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    # age_entry_modif.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    # adresse_entry_modif.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    # code_postal_entry_modif.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    # ville_entry_modif.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    # telephone_entry_modif.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    # mail_entry_modif.grid(row=7, column=1, padx=10, pady=5, sticky="w")


# Variable pour suivre le mode actuel
edit_mode = False

# Création des widgets pour le mode "copie"
nom_label = ttk.Label(tab3, text="Nom")
nom_button = ttk.Button(tab3, text="Nom", command=lambda: copy_to_clipboard("Nom"))

prenom_label = ttk.Label(tab3, text="Prénom")
prenom_button = ttk.Button(tab3, text="Prénom", command=lambda: copy_to_clipboard("Prénom"))

age_label = ttk.Label(tab3, text="Age")
age_button = ttk.Button(tab3, text="Age", command=lambda: copy_to_clipboard("Age"))

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

membre_ca_var = tk.BooleanVar()
membre_ca_check = ttk.Checkbutton(tab3, text="Membre CA", variable=membre_ca_var)

entre_nous_var = tk.BooleanVar()
entre_nous_check = ttk.Checkbutton(tab3, text="Entre nous", variable=entre_nous_var)

submit_button = ttk.Button(tab3, text="Valider", command=submit_form)

modify_button = ttk.Button(tab3, text="Modifier", command=switch_mode)


# ******* Création des widgets pour le mode "édition" *******

nom_label_modif = ttk.Label(tab3, text="Nom")
nom_entry_modif = ttk.Entry(tab3)

prenom_label_modif = ttk.Label(tab3, text="Prénom")
prenom_entry_modif = ttk.Entry(tab3)

age_label_modif = ttk.Label(tab3, text="Age")
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
        widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")

# Initialement, affichez les widgets en mode "copie"
#show_copy_widgets()


# Lancement de la boucle principale
root.mainloop()

