import tkinter as tk
from tkinter import ttk
import requests
from ttkbootstrap import Style
from tkinter import messagebox

# Fonction pour effectuer la recherche de codes postaux
def rechercher_code_postal(event=None):
    global code_postal
    code_postal = combobox_code_postal.get()

    # if code_postal:
    #     # URL de l'API d'adresse avec le paramètre "q" pour la recherche de code postal
    #     url = f"https://api-adresse.data.gouv.fr/search/?q={code_postal}&type=postcode&limit=5"
    #
    #     # Effectuer la requête GET à l'API
    #     response = requests.get(url)
    #
    #     # Vérifier si la requête a réussi
    #     if response.status_code == 200:
    #         data = response.json()
    #         ajouter_resultats_code_postal(data)
    #     else:
    #         messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")
    # else:
    #     messagebox.showwarning("Code postal manquant", "Veuillez entrer un code postal.")

# Fonction pour ajouter les résultats de codes postaux à la combobox
def ajouter_resultats_code_postal(data):
    if data.get('features'):
        resultats = []
        for feature in data['features']:
            properties = feature.get('properties', {})
            code_postal = properties.get('postcode', 'Code postal non trouvé')
            resultats.append(code_postal)
        combobox_code_postal['values'] = resultats
        combobox_code_postal.current(0)
    else:
        messagebox.showwarning("Aucun résultat", "Aucun code postal trouvé pour cette recherche.")

# Fonction pour effectuer la recherche de villes
def rechercher_ville(event=None):
    global ville
    code_postal = combobox_code_postal.get()
    ville = combobox_ville.get()

    if code_postal and ville:
        # URL de l'API d'adresse avec les paramètres "postcode" et "q" pour la recherche de ville
        url = f"https://api-adresse.data.gouv.fr/search/?q={ville}&postcode={code_postal}&type=locality&limit=5"

        # Effectuer la requête GET à l'API
        response = requests.get(url)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            ajouter_resultats_ville(data)
        else:
            messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")
    else:
        messagebox.showwarning("Ville manquante", "Veuillez entrer une ville.")

# Fonction pour ajouter les résultats de villes à la combobox
def ajouter_resultats_ville(data):
    if data.get('features'):
        resultats = []
        for feature in data['features']:
            properties = feature.get('properties', {})
            ville = properties.get('city', 'Ville non trouvée')
            resultats.append(ville)
        combobox_ville['values'] = resultats
        combobox_ville.current(0)
    else:
        messagebox.showwarning("Aucun résultat", "Aucune ville trouvée pour cette recherche.")

# Fonction pour effectuer la recherche de rues
def rechercher_rue(event=None):
    global rue
    code_postal = combobox_code_postal.get()
    ville = combobox_ville.get()
    rue = combobox_rue.get()

    if code_postal and ville and rue:
        # URL de l'API d'adresse avec les paramètres "postcode", "city" et "q" pour la recherche de rue
        url = f"https://api-adresse.data.gouv.fr/search/?q={rue}&postcode={code_postal}&city={ville}&type=street&limit=5"

        # Effectuer la requête GET à l'API
        response = requests.get(url)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            ajouter_resultats_rue(data)
        else:
            messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")
    else:
        messagebox.showwarning("Rue manquante", "Veuillez entrer une rue.")

# Fonction pour ajouter les résultats de rues à la combobox
def ajouter_resultats_rue(data):
    if data.get('features'):
        resultats = []
        for feature in data['features']:
            properties = feature.get('properties', {})
            adresse2 = properties.get('label', 'Adresse non trouvée')
            resultats.append(adresse2)
        adresse3 = [rue]
        print(adresse3, resultats)
        print(adresse3 + resultats)
        combobox_code_postal['values'] = adresse3 + resultats
        combobox_code_postal.current(0)
    else:
        messagebox.showwarning("Aucun résultat", "Aucune adresse trouvée pour cette recherche.")

# Fonction pour obtenir l'indice de l'élément sélectionné
def get_selected_index(event):
    index = combobox_ville .current()
    print(f"L'élément sélectionné est à l'indice : {index}")
    if index > 0:
        print("enregistrer le code postal et la ville")


# Création de la fenêtre principale avec ttkbootstrap
root = tk.Tk()
root.title("Recherche d'adresse en France")
style = Style(theme='vapor')

# Conteneur principal
frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Menu déroulant pour saisir et afficher les résultats de code postal
label_code_postal = ttk.Label(frame, text="Entrez un code postal:")
label_code_postal.grid(row=0, column=0, padx=10, pady=10)
combobox_code_postal = ttk.Combobox(frame, width=60)
combobox_code_postal.grid(row=0, column=1, padx=10, pady=10)
combobox_code_postal.bind("<Return>", rechercher_code_postal)

# Menu déroulant pour saisir et afficher les résultats de ville
label_ville = ttk.Label(frame, text="Entrez une ville:")
label_ville.grid(row=1, column=0, padx=10, pady=10)
combobox_ville = ttk.Combobox(frame, width=60)
combobox_ville.grid(row=1, column=1, padx=10, pady=10)
combobox_ville.bind("<Return>", rechercher_ville)
# Lier l'événement de sélection à la fonction
combobox_ville.bind("<<ComboboxSelected>>", get_selected_index)

# Menu déroulant pour saisir et afficher les résultats de rue
label_rue = ttk.Label(frame, text="Entrez une rue:")
label_rue.grid(row=2, column=0, padx=10, pady=10)
combobox_rue = ttk.Combobox(frame, width=60)
combobox_rue.grid(row=2, column=1, padx=10, pady=10)
combobox_rue.bind("<Return>", rechercher_rue)

# Lancer l'interface
root.mainloop()
