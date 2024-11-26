import tkinter as tk
from tkinter import ttk
import sqlite3
from ttkbootstrap import Style

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
    # Efface toutes les lignes actuelles dans le tableau
    for row in tableau.get_children():
        tableau.delete(row)

    # Utiliser les données fournies ou charger depuis SQLite si non fournies
    if data is None:
        data = charger_donnees()

    # Insère les données dans le tableau avec un séparateur visuel
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
    else:
        col_index = colonnes.index(colonne)
        for row in data:
            if recherche.lower() in str(row[col_index]).lower():
                resultats.append(row)

    mettre_a_jour_tableau(resultats)


# Création de la fenêtre principale
root = tk.Tk()
root.title("Tableau avec SQLite et ttkbootstrap")

# Ouvrir la fenêtre en plein écran
root.state('zoomed')

# Configuration du style ttkbootstrap
style = Style(theme='vapor')

# Configurer le style pour Treeview avec une hauteur de ligne augmentée
style.configure('Treeview', rowheight=40)  # Augmentez la valeur de rowheight pour une épaisseur de ligne plus grande

# Configurer le style pour la ligne sélectionnée
style.map('Treeview', background=[('selected', style.colors.secondary)], foreground=[('selected', 'white')])


# Configuration du tableau avec ttkbootstrap
colonnes = ["id", "nom", "prénom", "age", "adresse", "code postal", "ville", "telephone", "mail",
            "type", "activité", "cotisation", "montant", "don", "membre ca", "adresse",
            "recevoir_entre_nous", "date_paiement", "commentaire"]

# Frame de recherche
frame_recherche = ttk.Frame(root)
frame_recherche.pack(padx=10, pady=10, fill=tk.X)

# Variables de recherche
recherche_var = tk.StringVar()
colonne_var = tk.StringVar()

# Entrée de recherche
entry_recherche = ttk.Entry(frame_recherche, textvariable=recherche_var, width=50)
entry_recherche.pack(side=tk.LEFT, padx=5)

# Bouton de recherche avec icône de loupe
btn_recherche = ttk.Button(frame_recherche, text="🔍", style="secondary.Toolbutton.TButton", command=rechercher)
btn_recherche.pack(side=tk.LEFT, padx=5)

# Menu déroulant pour sélectionner la colonne ou "Tout"
menu_colonnes = ttk.Combobox(frame_recherche, textvariable=colonne_var, values=["Tout"] + colonnes, state='readonly')
menu_colonnes.set("Tout")
menu_colonnes.pack(side=tk.LEFT, padx=5)

# # Menu déroulant pour sélectionner la colonne
# menu_colonnes = ttk.Combobox(frame_recherche, textvariable=colonne_var, values=colonnes, state='readonly')
# menu_colonnes.set("Sélectionner une colonne")
# menu_colonnes.pack(side=tk.LEFT, padx=5)




# Frame principale avec un style ttkbootstrap
frame_principal = ttk.Frame(root)
frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Création du tableau avec une scrollbar verticale
scrollbar_y = ttk.Scrollbar(frame_principal)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

# Création du tableau avec une scrollbar horizontale
scrollbar_x = ttk.Scrollbar(frame_principal, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)


# Configuration du tableau avec ttkbootstrap
tableau = ttk.Treeview(frame_principal, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9",
                                                 "col10","col11", "col12", "col13", "col13.2", "col14", "col15", "col16", "col17",
                                                 "col18"), show="headings",
                       yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Configurer les en-têtes de colonnes
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
tableau.heading("col13.2", text="don")
tableau.heading("col14", text="membre ca")
tableau.heading("col15", text="adresse")
tableau.heading("col16", text="recevoir_entre_nous")
tableau.heading("col17", text="date_paiement")
tableau.heading("col18", text="commentaire")

# Affichage des lignes séparatrices avec ttkbootstrap
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

# Configurer les tags pour les lignes paires et impaires
tableau.tag_configure('evenrow', background='#330066')
tableau.tag_configure('oddrow', background='#4d0099')

# Configurer la police du tableau pour agrandir les lignes
style.configure('Treeview', rowheight=25, font=('Helvetica', 12))

# Ajouter les données initiales au tableau avec un séparateur visuel
mettre_a_jour_tableau()

# Configuration de la scrollbar pour le scrolling vertical
scrollbar_y.config(command=tableau.yview)
scrollbar_x.config(command=tableau.xview)
tableau.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# Bouton pour mettre à jour le tableau avec les données de la base de données
btn_maj = ttk.Button(frame_principal, text="Mettre à jour le tableau", style="primary.Outline.TButton",
                     command=mettre_a_jour_tableau)
btn_maj.pack(pady=10)

# Lancer l'application
root.mainloop()
