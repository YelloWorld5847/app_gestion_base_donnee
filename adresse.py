import requests

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from ttkbootstrap import Style


# Fonction pour effectuer la recherche d'adresse par rue
def rechercher_par_rue(widget_menu):
    code_postal = entry_code_postal.get().strip()
    rue = entry_rue.get().strip()
    rue_pour_url = rue.replace(" ", "+")
    print(rue_pour_url)

    if not rue:
        messagebox.showwarning("Champ manquant", "Veuillez entrer un nom de rue.")
        return

    base_url = "https://api-adresse.data.gouv.fr/search/?"
    params = [f"q={rue_pour_url}"]

    if code_postal:
        params.append(f"postcode={code_postal}")

    query_url = base_url + "&".join(params) + "&type=street" + "&limit=5"
    print(query_url)

    # Effectuer la requête GET à l'API
    response = requests.get(query_url)

    if response.status_code == 200:
        data = response.json()
        for feature in data['features']:
            properties = feature['properties']
            text_rue = properties['street']
            print(text_rue)
    else:
        messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")



# Fonction pour effectuer la recherche d'adresse par ville
def rechercher_par_ville(widget_menu):
    code_postal = entry_code_postal.get().strip()
    ville = entry_ville.get().strip()
    ville_pour_url = ville.replace(" ", "+")

    if not ville:
        messagebox.showwarning("Champ manquant", "Veuillez entrer un nom de ville.")
        return

    url = "https://api-adresse.data.gouv.fr/search/?"
    params = [f"q={ville_pour_url}"]

    if code_postal:
        params.append(f"postcode={code_postal}")

    query_url = url + "&".join(params) + "&type=municipality" + "&limit=5"
    print(query_url)

    # Effectuer la requête GET à l'API
    response = requests.get(query_url)

    if response.status_code == 200:
        data = response.json()
        for feature in data['features']:
            properties = feature['properties']
            text_rue = properties['label']
            print(text_rue)
    else:
        messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")

    # if response.status_code == 200:             type=municipality
    #     data = response.json()
    #     afficher_resultats(widget_menu, data)
    # else:
    #     messagebox.showerror("Erreur", f"Erreur {response.status_code} lors de la requête à l'API.")


# Fonction pour afficher les résultats dans le menu déroulant spécifié
def afficher_resultats(widget_menu, data):
    widget_menu.delete(0, tk.END)  # Effacer les résultats précédents
    if data.get('features'):
        for feature in data['features']:
            properties = feature.get('properties', {})
            adresse = properties.get('label', 'Adresse non trouvée')
            widget_menu.insert(tk.END, adresse)
    else:
        messagebox.showwarning("Aucun résultat", "Aucune adresse trouvée pour cette recherche.")


# Création de la fenêtre principale avec ttkbootstrap
root = tk.Tk()
root.title("Recherche d'adresse en France")
style = Style(theme='vapor')

# Conteneur principal
frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Entrée pour le code postal
label_code_postal = ttk.Label(frame, text="Code Postal:")
label_code_postal.grid(row=0, column=0, padx=10, pady=10)
entry_code_postal = ttk.Entry(frame, width=30)
entry_code_postal.grid(row=0, column=1, padx=10, pady=10)

# Entrée pour la ville
label_ville = ttk.Label(frame, text="Ville:")
label_ville.grid(row=1, column=0, padx=10, pady=10)
entry_ville = ttk.Entry(frame, width=30)
entry_ville.grid(row=1, column=1, padx=10, pady=10)

# Entrée pour la rue
label_rue = ttk.Label(frame, text="Rue:")
label_rue.grid(row=2, column=0, padx=10, pady=10)
entry_rue = ttk.Entry(frame, width=30)
entry_rue.grid(row=2, column=1, padx=10, pady=10)

# Bouton de recherche par ville
bouton_rechercher_ville = ttk.Button(frame, text="Rechercher Ville")
bouton_rechercher_ville.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
bouton_rechercher_ville.configure(command=lambda: rechercher_par_ville(combobox_resultats))

# Bouton de recherche par rue
bouton_rechercher_rue = ttk.Button(frame, text="Rechercher Rue")
bouton_rechercher_rue.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
bouton_rechercher_rue.configure(command=lambda: rechercher_par_rue(combobox_resultats))

# Menu déroulant pour afficher les résultats
combobox_resultats = tk.Listbox(frame, height=10, width=60)
combobox_resultats.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Lancer l'interface
root.mainloop()