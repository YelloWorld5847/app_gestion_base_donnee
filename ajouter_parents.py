import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import *


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
        "date_paiement": date_DateEntry.entry.get(),
        "commentaire": commentaire_text.get("1.0", tk.END),
        "membre_ca": membre_ca_var.get(),
        "recevoir_entre_nous": entre_nous_var.get()
    }

    conn = sqlite3.connect('association.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO parents (nom, prenom, age, adresse, code_postal, ville, telephone, mail, type, activite, cotisation, montant, don, mode_paiement, date_paiement, commentaire, membre_ca, recevoir_entre_nous)
        VALUES (:nom, :prenom, :age, :adresse, :code_postal, :ville, :telephone, :mail, :type, :activite, :cotisation, :montant, :don, :mode_paiement, :date_paiement, :commentaire, :membre_ca, :recevoir_entre_nous)
    ''', data)
    conn.commit()
    conn.close()

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
            print("boucle 3")
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

            print(f"x_test : {x_test} | y_test : {y_test}")

            for key, value in child_windows.items():
                print(f"key : {key}")
                print(f"pos x à tester : {child_windows[key]["x"]}")
                print(f"pos y à tester : {child_windows[key]["y"]}")
                if x_f == child_windows[key]["x"] and y_f == child_windows[key]["y"]:
                    print("**** break *****")
                    peux_placer = False

            if peux_placer:
                print("peux placerreste reste à `  TRUE   `")
                peux_placer_end = True
                break
            else:
                print("peux placer à été mit à  `  FALSE   `")
        x_f_a += ESPACEMENT_X
        y_f_a += ESPACEMENT_Y
        #print("---------print ok-------------")



    print("\n")
    print(nomb_fenetre2)
    print("\n")
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

        "age_label": ttk.Label(new_window, text="Age"),
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
        "type_combobox": ttk.Combobox(new_window, values=["AVT", "AF", "PRO", "ASS", "PA", "Bénévole", "PA AUT"]),

        "activite_label": ttk.Label(new_window, text="Activité"),
        "activite_combobox": ttk.Combobox(new_window, values=["Option 1", "Option 2"]),

        "cotisation_label": ttk.Label(new_window, text="Cotisation"),
        "cotisation_entry": ttk.Entry(new_window),

        "montant_label": ttk.Label(new_window, text="Montant"),
        "montant_spinbox": ttk.Spinbox(new_window, from_=0, to=1000000000000000000000000000000000),

        "don_label": ttk.Label(new_window, text="don"),
        "don_spinbox": ttk.Spinbox(new_window, from_=0, to=1000000000000000000000000000000000),

        "mode_paiement_label": ttk.Label(new_window, text="Mode paiement"),
        "mode_paiement_combobox": ttk.Combobox(new_window, values=["Option 1", "Option 2"]),

        "dt": datetime.now().date(),
        "date_label": ttk.Label(new_window, text="Date paiement"),
        "date_DateEntry": ttk.DateEntry(new_window, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY),

        "commentaire_label": ttk.Label(new_window, text="Commentaire"),
        "commentaire_text": tk.Text(new_window, height=5, width=40),

        "membre_ca_var": tk.BooleanVar(),
        "membre_ca_check": ttk.Checkbutton(new_window, text="Membre CA", variable=membre_ca_var),

        "entre_nous_var": tk.BooleanVar(),
        "entre_nous_check": ttk.Checkbutton(new_window, text="Entre nous", variable=entre_nous_var),

        "submit_button": ttk.Button(new_window, text="Valider", command=submit_form),

        "ajouter_enfant": ttk.Button(new_window, text="Ouvrir une nouvelle fenêtre", command=open_new_window),
    }

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
        (child_windows[nomb_fenetre2]["submit_button"], 9, 2), (child_windows[nomb_fenetre2]["ajouter_enfant"], 9, 3)
    ]

    for widget in widgets:
        if len(widget) == 3:
            widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
        elif len(widget) == 5:
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5,
                           sticky="w")


    child_windows = dict(sorted(child_windows.items()))


    print(child_windows)

    # Réinitialiser la taille et la position de la nouvelle fenêtre
    new_window.geometry(f"+{x_f}+{y_f}")

    pos_fnt_avant_plan = nomb_fenetre % 3
    print(f"position fenêtre à mettre avant plan : {pos_fnt_avant_plan}")

    for key, value in child_windows.items():
        if value["pos"] == pos:
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

# Création de la fenêtre principale
root = ttk.Window(themename="vapor")
root.title("Formulaire d'inscription")
root.state('zoomed')


# ---------------- Onglet Ajouter Utilisateur ---------------- #
nom_label = ttk.Label(root, text="Nom")
nom_entry = ttk.Entry(root, width=30)

prenom_label = ttk.Label(root, text="Prénom")
prenom_entry = ttk.Entry(root)

age_label = ttk.Label(root, text="Age")
age_entry = ttk.Entry(root)

adresse_label = ttk.Label(root, text="Adresse")
adresse_entry = ttk.Entry(root, width=30)

code_postal_label = ttk.Label(root, text="Code postal")
code_postal_entry = ttk.Entry(root)

ville_label = ttk.Label(root, text="Ville")
ville_entry = ttk.Entry(root)

telephone_label = ttk.Label(root, text="Téléphone")
telephone_entry = ttk.Entry(root)

mail_label = ttk.Label(root, text="Mail")
mail_entry = ttk.Entry(root)

type_label = ttk.Label(root, text="Type")
type_combobox = ttk.Combobox(root, values=["AVT", "AF", "PRO", "ASS", "PA", "Bénévole", "PA AUT"])

activite_label = ttk.Label(root, text="Activité")
activite_combobox = ttk.Combobox(root, values=["Option 1", "Option 2"])

cotisation_label = ttk.Label(root, text="Cotisation")
cotisation_entry = ttk.Entry(root)

montant_label = ttk.Label(root, text="Montant")
montant_spinbox = ttk.Spinbox(root, from_=0, to=1000000000000000000000000000000000)

don_label = ttk.Label(root, text="don")
don_spinbox = ttk.Spinbox(root, from_=0, to=1000000000000000000000000000000000)

mode_paiement_label = ttk.Label(root, text="Mode paiement")
mode_paiement_combobox = ttk.Combobox(root, values=["Option 1", "Option 2"])

dt = datetime.now().date()
date_label = ttk.Label(root, text="Date paiement")
date_DateEntry = ttk.DateEntry(root, dateformat='%Y-%m-%d', firstweekday=2, startdate=dt, bootstyle=PRIMARY)

commentaire_label = ttk.Label(root, text="Commentaire")
commentaire_text = tk.Text(root, height=5, width=40)

membre_ca_var = tk.BooleanVar()
membre_ca_check = ttk.Checkbutton(root, text="Membre CA", variable=membre_ca_var)

entre_nous_var = tk.BooleanVar()
entre_nous_check = ttk.Checkbutton(root, text="Entre nous", variable=entre_nous_var)

submit_button = ttk.Button(root, text="Valider", command=submit_form)

ajouter_enfant = ttk.Button(root, text="Ouvrir une nouvelle fenêtre", command=open_new_window)

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
    (submit_button, 9, 2), (ajouter_enfant, 9, 3)
]

for widget in widgets:
    if len(widget) == 3:
        widget[0].grid(row=widget[1], column=widget[2], padx=10, pady=5, sticky="w")
    elif len(widget) == 5:
        widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3], rowspan=widget[4], padx=10, pady=5, sticky="w")


# Lancement de la boucle principale
root.mainloop()
