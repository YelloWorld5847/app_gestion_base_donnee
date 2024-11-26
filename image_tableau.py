import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Fonction pour récupérer les informations de l'élément sélectionné
def on_select(event):
    selected_item = tree.selection()[0]  # Récupère l'ID de l'élément sélectionné
    item = tree.item(selected_item)  # Récupère les détails de l'élément
    print(item)

# Créer la fenêtre principale
root = ttk.Window(themename="vapor")

# Créer un Treeview avec une colonne d'arborescence
tree = ttk.Treeview(root, columns=("name",), show='tree headings')
tree.heading("#0", text="Name")
tree.heading("name", text="Details")

# Insérer des données avec une structure hiérarchique
parent = tree.insert("", "end", text="Parent", values=("Parent Details",), open=True)
child1 = tree.insert(parent, "end", text="Child 1", values=("Child 1 Details",))
child2 = tree.insert(parent, "end", text="Child 2", values=("Child 2 Details",))

parent2 = tree.insert("", "end", text="Parent", values=("Parent Details",), open=True)
child3 = tree.insert(parent2, "end", text="Child 1", values=("Child 1 Details",))
child4 = tree.insert(parent2, "end", text="Child 2", values=("Child 2 Details",))

# Attacher l'événement de sélection
tree.bind("<<TreeviewSelect>>", on_select)

# Placer le Treeview dans la fenêtre
tree.pack(fill=BOTH, expand=YES)

# Lancer l'application
root.mainloop()
