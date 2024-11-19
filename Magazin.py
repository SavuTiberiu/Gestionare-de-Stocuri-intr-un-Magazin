import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Conexiune la baza de date
def connect_db():
    global conn, cursor
    conn = sqlite3.connect("magazin.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vanzator
                      (id INTEGER PRIMARY KEY, nume TEXT, functie TEXT, salariu REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS produse
                      (id INTEGER PRIMARY KEY, nume TEXT, pret REAL, stoc INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comenzi
                      (id INTEGER PRIMARY KEY, data TEXT, vanzator_id INTEGER,
                      FOREIGN KEY (vanzator_id) REFERENCES vanzator(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalii_comanda
                      (comanda_id INTEGER, produs_id INTEGER, cantitate INTEGER,
                      FOREIGN KEY (comanda_id) REFERENCES comenzi(id),
                      FOREIGN KEY (produs_id) REFERENCES produse(id))''')
    conn.commit()

# Adăugarea unui vânzător
def add_vanzator():
    nume = nume_initial.get()
    functie = functie_initial.get()
    salariu = salariu_initial.get()
    if nume and functie and salariu:
        cursor.execute("INSERT INTO vanzator (nume, functie, salariu) VALUES(?,?,?)", (nume, functie, float(salariu)))
        conn.commit()
        messagebox.showinfo("Succes!", "Vanzatorul a fost adaugat.")
        clear_entries_vanzator()
        query_vanzator()
    else:
        messagebox.showerror("Eroare", "Nu ati completat tot.")

# Adăugarea unui produs
def add_produs():
    nume = nume_produs.get()
    pret = pret_produs.get()
    stoc = stoc_produs.get()
    if nume and pret and stoc:
        cursor.execute("INSERT INTO produse (nume, pret, stoc) VALUES(?,?,?)", (nume, float(pret), int(stoc)))
        conn.commit()
        messagebox.showinfo("Succes!", "Produsul a fost adaugat.")
        clear_entries_produs()
        query_produs()
    else:
        messagebox.showerror("Eroare", "Nu ati completat tot.")

# Interogarea vânzătorilor
def query_vanzator():
    search_term = search_vanzator_entry.get()
    if search_term:
        cursor.execute("SELECT * FROM vanzator WHERE nume LIKE ?", ('%' + search_term + '%',))
    else:
        cursor.execute("SELECT * FROM vanzator")
    rows = cursor.fetchall()
    update_treeview(tree_vanzator, rows)

# Interogarea produselor
def query_produs():
    search_term = search_produs_entry.get()
    if search_term:
        cursor.execute("SELECT * FROM produse WHERE nume LIKE ?", ('%' + search_term + '%',))
    else:
        cursor.execute("SELECT * FROM produse")
    rows = cursor.fetchall()
    update_treeview(tree_produs, rows)

def update_treeview(treeview, rows):
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", tk.END, values=row)

# Golirea câmpurilor de introducere pentru vânzători
def clear_entries_vanzator():
    nume_initial.delete(0, tk.END)
    functie_initial.delete(0, tk.END)
    salariu_initial.delete(0, tk.END)

# Golirea câmpurilor de introducere pentru produse
def clear_entries_produs():
    nume_produs.delete(0, tk.END)
    pret_produs.delete(0, tk.END)
    stoc_produs.delete(0, tk.END)

# Închiderea conexiunii la baza de date
def close_db():
    conn.close()
    root.destroy()

# Funcție de editare vânzător
def edit_vanzator():
    selected_item = tree_vanzator.selection()
    if selected_item:
        id_vanzator = tree_vanzator.item(selected_item)["values"][0]  # Obținem ID-ul din primul element al listei de valori
        nume = nume_initial.get()
        functie = functie_initial.get()
        salariu = salariu_initial.get()
        if nume and functie and salariu:
            cursor.execute("UPDATE vanzator SET nume=?, functie=?, salariu=? WHERE id=?", (nume, functie, float(salariu), id_vanzator))
            conn.commit()
            messagebox.showinfo("Succes!", "Vânzătorul a fost modificat.")
            clear_entries_vanzator()
            query_vanzator()
        else:
            messagebox.showerror("Error", "Nu ați completat toate câmpurile.")
    else:
        messagebox.showerror("Error", "Selectați un vânzător pentru a-l modifica.")

# Funcție de ștergere vânzător
def delete_vanzator():
    selected_item = tree_vanzator.selection()
    if selected_item:
        id_vanzator = tree_vanzator.item(selected_item)["values"][0]  # Obținem ID-ul din primul element al listei de valori
        cursor.execute("DELETE FROM vanzator WHERE id=?", (id_vanzator,))
        conn.commit()
        messagebox.showinfo("Succes!", "Vânzătorul a fost șters.")
        query_vanzator()  # Reîmprospătăm tabelul vânzători
    else:
        messagebox.showerror("Error", "Selectati un vanzator pentru a-l sterge.")

# Funcție de editare produs
def edit_produs():
    selected_item = tree_produs.selection()
    if selected_item:
        id_produs = tree_produs.item(selected_item)["values"][0]  # Obținem ID-ul din primul element al listei de valori
        nume = nume_produs.get()
        pret = pret_produs.get()
        stoc = stoc_produs.get()
        if nume and pret and stoc:
            cursor.execute("UPDATE produse SET nume=?, pret=?, stoc=? WHERE id=?", (nume, float(pret), int(stoc), id_produs))
            conn.commit()
            messagebox.showinfo("Succes!", "Produsul a fost modificat.")
            clear_entries_produs()
            query_produs()
        else:
            messagebox.showerror("Error", "Nu ați completat toate câmpurile.")
    else:
        messagebox.showerror("Error", "Selectați un produs pentru a-l modifica.")

# Funcție de ștergere produs
def delete_produs():
    selected_item = tree_produs.selection()
    if selected_item:
        id_produs = tree_produs.item(selected_item)["values"][0]  # Obținem ID-ul din primul element al listei de valori
        cursor.execute("DELETE FROM produse WHERE id=?", (id_produs,))
        conn.commit()
        messagebox.showinfo("Succes!", "Produsul a fost șters.")
        query_produs()  # Reîmprospătăm tabelul produse
    else:
        messagebox.showerror("Error", "Selectati un produs pentru a-l sterge.")

# Crearea interfeței grafice
root = tk.Tk()
root.title("Baza de date magazin")

# Stilizare
style = ttk.Style()
style.configure("TFrame", padding=10)
style.configure("TButton", padding=5)
style.configure("TLabel", padding=5)
style.configure("TEntry", padding=5)
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 10))

# Tabel angajati
ttk.Label(root, text="Tabel angajați", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
frame_vanzator = ttk.Frame(root)
frame_vanzator.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
frame_vanzator.grid_rowconfigure(0, weight=1)
frame_vanzator.grid_columnconfigure(0, weight=1)

tree_vanzator = ttk.Treeview(frame_vanzator, columns=("ID", "Nume", "Funcție", "Salariu"))
tree_vanzator.heading("#0", text="", anchor=tk.W)
tree_vanzator.heading("ID", text="ID", anchor=tk.W)
tree_vanzator.heading("Nume", text="Nume", anchor=tk.W)
tree_vanzator.heading("Funcție", text="Funcție", anchor=tk.W)
tree_vanzator.heading("Salariu", text="Salariu", anchor=tk.W)
tree_vanzator.column("#0", stretch=tk.NO, minwidth=0, width=0)
tree_vanzator.column("ID", stretch=tk.NO, minwidth=0, width=50)
tree_vanzator.column("Nume", stretch=tk.NO, minwidth=0, width=150)
tree_vanzator.column("Funcție", stretch=tk.NO, minwidth=0, width=150)
tree_vanzator.column("Salariu", stretch=tk.NO, minwidth=0, width=100)
tree_vanzator.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

scrollbar_vanzator = ttk.Scrollbar(frame_vanzator, orient="vertical", command=tree_vanzator.yview)
scrollbar_vanzator.grid(row=0, column=1, sticky="ns")
tree_vanzator.configure(yscrollcommand=scrollbar_vanzator.set)

ttk.Label(root, text="Adaugare angajat in tabel", font=("Helvetica", 12, "bold")).grid(row=2, column=0, padx=10, pady=(20, 10), sticky="w")

frame_inputs_vanzator = ttk.Frame(root)
frame_inputs_vanzator.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_inputs_vanzator, text="Nume:").grid(row=0, column=0, sticky=tk.W)
nume_initial = ttk.Entry(frame_inputs_vanzator)
nume_initial.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_inputs_vanzator, text="Funcție:").grid(row=1, column=0, sticky=tk.W)
functie_initial = ttk.Entry(frame_inputs_vanzator)
functie_initial.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_inputs_vanzator, text="Salariu:").grid(row=2, column=0, sticky=tk.W)
salariu_initial = ttk.Entry(frame_inputs_vanzator)
salariu_initial.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(frame_inputs_vanzator, text="Adaugă Vânzător", command=add_vanzator).grid(row=3, column=0, columnspan=2, pady=10)

# Butoane pentru acțiuni vânzători
frame_actions_vanzator = ttk.Frame(root)
frame_actions_vanzator.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_actions_vanzator, text="Acțiuni Vânzători", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
ttk.Button(frame_actions_vanzator, text="Modifică", command=edit_vanzator).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame_actions_vanzator, text="Șterge", command=delete_vanzator).grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_actions_vanzator, text="Caută:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W)
search_vanzator_entry = ttk.Entry(frame_actions_vanzator)
search_vanzator_entry.grid(row=2, column=1, pady=5)
ttk.Button(frame_actions_vanzator, text="Caută", command=query_vanzator).grid(row=3, column=0, pady=10)
ttk.Button(frame_actions_vanzator, text="Reset", command=query_vanzator).grid(row=3, column=1, pady=10)

# Tabel produse
ttk.Label(root, text="Tabel produse", font=("Helvetica", 16, "bold")).grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="w")
frame_produs = ttk.Frame(root)
frame_produs.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
frame_produs.grid_rowconfigure(0, weight=1)
frame_produs.grid_columnconfigure(0, weight=1)

tree_produs = ttk.Treeview(frame_produs, columns=("ID", "Nume", "Preț", "Stoc"))
tree_produs.heading("#0", text="", anchor=tk.W)
tree_produs.heading("ID", text="ID", anchor=tk.W)
tree_produs.heading("Nume", text="Nume", anchor=tk.W)
tree_produs.heading("Preț", text="Preț", anchor=tk.W)
tree_produs.heading("Stoc", text="Stoc", anchor=tk.W)
tree_produs.column("#0", stretch=tk.NO, minwidth=0, width=0)
tree_produs.column("ID", stretch=tk.NO, minwidth=0, width=50)
tree_produs.column("Nume", stretch=tk.NO, minwidth=0, width=150)
tree_produs.column("Preț", stretch=tk.NO, minwidth=0, width=100)
tree_produs.column("Stoc", stretch=tk.NO, minwidth=0, width=100)
tree_produs.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

scrollbar_produs = ttk.Scrollbar(frame_produs, orient="vertical", command=tree_produs.yview)
scrollbar_produs.grid(row=0, column=1, sticky="ns")
tree_produs.configure(yscrollcommand=scrollbar_produs.set)

ttk.Label(root, text="Adaugare produs in tabel", font=("Helvetica", 12, "bold")).grid(row=2, column=2, padx=10, pady=(20, 10), sticky="w")

frame_inputs_produs = ttk.Frame(root)
frame_inputs_produs.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_inputs_produs, text="Nume:").grid(row=0, column=0, sticky=tk.W)
nume_produs = ttk.Entry(frame_inputs_produs)
nume_produs.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_inputs_produs, text="Preț:").grid(row=1, column=0, sticky=tk.W)
pret_produs = ttk.Entry(frame_inputs_produs)
pret_produs.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_inputs_produs, text="Stoc:").grid(row=2, column=0, sticky=tk.W)
stoc_produs = ttk.Entry(frame_inputs_produs)
stoc_produs.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(frame_inputs_produs, text="Adaugă Produs", command=add_produs).grid(row=3, column=0, columnspan=2, pady=10)

# Butoane pentru acțiuni produse
frame_actions_produs = ttk.Frame(root)
frame_actions_produs.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_actions_produs, text="Acțiuni Produse", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
ttk.Button(frame_actions_produs, text="Modifică", command=edit_produs).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame_actions_produs, text="Șterge", command=delete_produs).grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_actions_produs, text="Caută:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W)
search_produs_entry = ttk.Entry(frame_actions_produs)
search_produs_entry.grid(row=2, column=1, pady=5)
ttk.Button(frame_actions_produs, text="Caută", command=query_produs).grid(row=3, column=0, pady=10)
ttk.Button(frame_actions_produs, text="Reset", command=query_produs).grid(row=3, column=1, pady=10)

# Butoane pentru acțiuni globale
frame_global_actions = ttk.Frame(root)
frame_global_actions.grid(row=4, column=3, padx=10, pady=10, sticky="se")

ttk.Button(frame_global_actions, text="Închide", command=close_db).grid(row=0, column=0, padx=5, pady=5)

# Meniu
meniu = tk.Menu(root)
root.config(menu=meniu)

meniu_fisier = tk.Menu(meniu, tearoff=0)
meniu.add_cascade(label="Fișier", menu=meniu_fisier)
meniu_fisier.add_command(label="Închide", command=close_db)

# Conectare la baza de date la pornirea aplicației
connect_db()
query_vanzator()
query_produs()

# Pornirea buclei principale
root.mainloop()
