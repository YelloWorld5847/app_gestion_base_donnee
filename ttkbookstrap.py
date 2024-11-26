import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

def create_widgets(root):
    # Créer un style bootstrap
    style = Style(theme='superhero')

    # Frame principale
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=BOTH, expand=True)

    # Label
    label = ttk.Label(main_frame, text="Exemple de ttkbootstrap", font=('Helvetica', 16))
    label.pack(pady=10)

    # Entry
    entry = ttk.Entry(main_frame)
    entry.insert(0, "Entrez du texte ici")
    entry.pack(pady=10)

    # Bouton
    button = ttk.Button(main_frame, text="Cliquez-moi", style='success.TButton')
    button.pack(pady=10)

    # Checkbutton
    checkbutton = ttk.Checkbutton(main_frame, text="Option 1")
    checkbutton.pack(pady=10)

    # Radiobuttons
    radiobutton1 = ttk.Radiobutton(main_frame, text="Option A", value=1)
    radiobutton2 = ttk.Radiobutton(main_frame, text="Option B", value=2)
    radiobutton1.pack(pady=10)
    radiobutton2.pack(pady=10)

    # Combobox
    combobox = ttk.Combobox(main_frame, values=["Choix 1", "Choix 2", "Choix 3"])
    combobox.pack(pady=10)

    # Spinbox
    spinbox = ttk.Spinbox(main_frame, from_=0, to=100000000000000000000000000000000000000000000)
    spinbox.pack(pady=10)

    # Scale
    scale = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL)
    scale.pack(pady=10)

    # Progressbar
    progressbar = ttk.Progressbar(main_frame, mode='determinate')
    progressbar.pack(pady=10)
    progressbar.start()

    # Notebook
    notebook = ttk.Notebook(main_frame)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab1, text='Tab 1')
    notebook.add(tab2, text='Tab 2')
    notebook.pack(pady=10, fill=BOTH, expand=True)

    # Treeview
    treeview = ttk.Treeview(main_frame, columns=("Column1", "Column2"), show='headings')
    treeview.heading("Column1", text="Colonne 1")
    treeview.heading("Column2", text="Colonne 2")
    treeview.insert("", "end", values=("Valeur 1", "Valeur 2"))
    treeview.pack(pady=10, fill=BOTH, expand=True)

    # PanedWindow
    panedwindow = ttk.PanedWindow(main_frame)
    panedwindow.pack(pady=10, fill=BOTH, expand=True)
    pane1 = ttk.Frame(panedwindow)
    pane2 = ttk.Frame(panedwindow)
    panedwindow.add(pane1)
    panedwindow.add(pane2)

    # Separator
    separator = ttk.Separator(main_frame, orient=HORIZONTAL)
    separator.pack(pady=10, fill=X)

    # Text
    text = tk.Text(main_frame, height=5)
    text.pack(pady=10, fill=BOTH, expand=True)
    text.insert(tk.END, "Ceci est un exemple de texte.")

    # Messagebox (juste un bouton pour déclencher)
    def show_message():
        style.messagebox.show_info("Titre", "Message d'information")

    message_button = ttk.Button(main_frame, text="Afficher message", command=show_message)
    message_button.pack(pady=10)

def main():
    root = tk.Tk()
    root.title("Exemple de ttkbootstrap")
    root.geometry("800x600")
    create_widgets(root)
    root.mainloop()

if __name__ == "__main__":
    main()
