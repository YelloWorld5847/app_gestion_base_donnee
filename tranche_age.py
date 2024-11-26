import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

# Liste pour garder les références des fenêtres enfant
child_windows = []


def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Nouvelle fenêtre")
    label = ttk.Label(new_window, text="Nouvelle fenêtre")
    label.pack(pady=20, padx=20)

    # Ajouter la nouvelle fenêtre à la liste des fenêtres enfant
    child_windows.append(new_window)

    # Définir la fenêtre enfant comme fenêtre supérieure
    new_window.attributes("-topmost", True)

    # Supprimer la référence de la liste lorsque la fenêtre est fermée
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_close(new_window))


def on_close(window):
    # Retirer la fenêtre de la liste avant de la détruire
    if window in child_windows:
        child_windows.remove(window)
    window.destroy()


root = ttkb.Window(themename="superhero")
root.title("Fenêtre Principale")

# Mettre la fenêtre principale en mode zoomed
root.state('zoomed')

button = ttkb.Button(root, text="Ouvrir une nouvelle fenêtre", command=open_new_window)
button.pack(pady=20, padx=20)

root.mainloop()
