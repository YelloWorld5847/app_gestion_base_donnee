import tkinter as tk
import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from datetime import datetime
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

# Fonction pour remplir les widgets du formulaire de modification
def remplir_formulaire(row):
    nom_entry_modif.delete(0, tk.END)
    nom_entry_modif.insert(0, row[1])
    prenom_entry_modif.delete(0, tk.END)
    prenom_entry_modif.insert(0, row[2])
    age_entry_modif.delete(0, tk.END)
    age_entry_modif.insert(0, row[3])
    adresse_entry_modif.delete(0, tk.END)
    adresse_entry_modif.insert(0, row[4])
    code_postal_entry_modif.delete(0, tk.END)
    code_postal_entry_modif.insert(0, row[5])
    ville_entry_modif.delete(0, tk.END)
    ville_entry_modif.insert(0, row[6])
    telephone_entry_modif.delete(0, tk.END)
    telephone_entry_modif.insert(0, row[7])
    mail_entry_modif.delete(0, tk.END)
    mail_entry_modif.insert(0, row[8])
    type_combobox_modif.set(row[9])
    activite_combobox_modif.set(row[10])
    cotisation_entry_modif.delete(0, tk.END)
    cotisation_entry_modif.insert(0, row[11])
    montant_spinbox_modif.delete(0, tk.END)
    montant_spinbox_modif.insert(0, row[12])
    don_spinbox_modif.delete(0, tk.END)
    don_spinbox_modif.insert(0, row[13])
    mode_paiement_combobox_modif.set(row[14])
    membre_ca_var_modif.set(row[15])
    entre_nous_var_modif.set(row[16])
    date_DateEntry_modif.entry.delete(0, tk.END)
    date_DateEntry_modif.entry.insert(0, row[17])
    commentaire_text_modif.delete("1.0", tk.END)
    commentaire_text_modif.insert(tk.END, row[18])
    notebook.select(tab3)
id_modif = None
# Fonction de gestion du double-clic sur une ligne du tableau
def on_double_click(event):
    global id_modif
    selected_item = tableau.selection()
    if selected_item:
        item = tableau.item(selected_item)
        id_modif = item['values'][0]
        print(id_modif)
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

widgets_modif = [
    (nom_label_modif, 0, 0), (nom_entry_modif, 0, 1),
    (prenom_label_modif, 1, 0), (prenom_entry_modif, 1, 1),
    (age_label_modif, 2, 0), (age_entry_modif, 2, 1),
    (adresse_label_modif, 3, 0), (adresse_entry_modif, 3, 1),
    (code_postal_label_modif, 4, 0), (code_postal_entry_modif, 4, 1),
    (ville_label_modif, 5, 0), (ville_entry_modif, 5, 1),
    (telephone_label_modif, 6, 0), (telephone_entry_modif, 6, 1),
    (mail_label_modif, 7, 0), (mail_entry_modif, 7, 1),
    (type_label_modif, 0, 2), (type_combobox_modif, 0, 3),
    (activite_label_modif, 1, 2), (activite_combobox_modif, 1, 3),
    (cotisation_label_modif, 2, 2), (cotisation_entry_modif, 2, 3),
    (montant_label_modif, 3, 2), (montant_spinbox_modif, 3, 3),
    (don_label_modif, 4, 2), (don_spinbox_modif, 4, 3),
    (mode_paiement_label_modif, 5, 2), (mode_paiement_combobox_modif, 5, 3),
    (date_label_modif, 6, 2), (date_DateEntry_modif, 6, 3),
    (commentaire_label_modif, 8, 0), (commentaire_text_modif, 8, 1, 1, 4),
    (membre_ca_check_modif, 7, 2), (entre_nous_check_modif, 7, 3),
    (submit_button_modif, 9, 3)
]

for widget in widgets_modif:
    if len(widget) == 3:
        widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")

# Lancement de la boucle principale
root.mainloop()

