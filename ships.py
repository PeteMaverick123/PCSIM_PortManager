import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path


# Databáze bude uložena vedle programu
DB_FILE = Path(__file__).with_name("port_city.db")


def connect_database():
    connection = sqlite3.connect(DB_FILE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS ships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ship_type TEXT NOT NULL,
            length REAL NOT NULL,
            capacity REAL NOT NULL
        )
    """)

    connection.commit()
    return connection


class ShipsWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Port City Simulator - Ships")
        self.window.geometry("950x600")
        self.window.configure(bg="#17232f")

        self.connection = connect_database()

        self.create_interface()
        self.load_ships()

        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def create_interface(self):

        # Nadpis
        header = tk.Frame(
            self.window,
            bg="#223342",
            height=75
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="SHIP REGISTRY",
            font=("Arial", 21, "bold"),
            fg="white",
            bg="#223342"
        ).pack(pady=20)

        # Formulář
        form = tk.LabelFrame(
            self.window,
            text=" Nová loď ",
            font=("Arial", 11, "bold"),
            fg="#36a6a0",
            bg="#17232f",
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=20, pady=15)

        tk.Label(
            form, text="Název lodi:",
            fg="white", bg="#17232f"
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.name_entry = tk.Entry(form, width=23)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(
            form, text="Typ lodě:",
            fg="white", bg="#17232f"
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.type_box = ttk.Combobox(
            form,
            values=[
                "Kontejnerová",
                "Nákladní",
                "Tanker",
                "Osobní",
                "Ro-Ro",
                "Vojenská",
                "Jiná"
            ],
            state="readonly",
            width=20
        )
        self.type_box.grid(row=1, column=1, padx=5, pady=5)
        self.type_box.current(0)

        tk.Label(
            form, text="Délka (m):",
            fg="white", bg="#17232f"
        ).grid(row=0, column=2, sticky="w", padx=5)

        self.length_entry = tk.Entry(form, width=15)
        self.length_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(
            form, text="Kapacita (t):",
            fg="white", bg="#17232f"
        ).grid(row=0, column=3, sticky="w", padx=5)

        self.capacity_entry = tk.Entry(form, width=15)
        self.capacity_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(
            form,
            text="Přidat loď",
            command=self.add_ship
        ).grid(row=2, column=0, columnspan=4, pady=12)

        # Tabulka
        table_frame = tk.Frame(
            self.window,
            bg="#17232f"
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columns = (
            "id", "name", "type", "length", "capacity"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Název lodi",
            "type": "Typ",
            "length": "Délka (m)",
            "capacity": "Kapacita (t)"
        }

        widths = {
            "id": 50,
            "name": 220,
            "type": 170,
            "length": 130,
            "capacity": 150
        }

        for column in columns:
            self.table.heading(
                column,
                text=headings[column]
            )
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.pack(fill="both", expand=True)

        ttk.Button(
            self.window,
            text="Odstranit vybranou loď",
            command=self.delete_ship
        ).pack(pady=12)

    def add_ship(self):

        name = self.name_entry.get().strip()
        ship_type = self.type_box.get()

        try:
            length = float(
                self.length_entry.get().replace(",", ".")
            )
            capacity = float(
                self.capacity_entry.get().replace(",", ".")
            )
        except ValueError:
            messagebox.showerror(
                "Chybný údaj",
                "Délka a kapacita musí být čísla."
            )
            return

        if not name or length <= 0 or capacity <= 0:
            messagebox.showerror(
                "Chybný údaj",
                "Vyplň název a zadej kladné hodnoty."
            )
            return

        self.connection.execute(
            """
            INSERT INTO ships
            (name, ship_type, length, capacity)
            VALUES (?, ?, ?, ?)
            """,
            (name, ship_type, length, capacity)
        )

        self.connection.commit()

        self.name_entry.delete(0, tk.END)
        self.length_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)

        self.load_ships()

    def load_ships(self):

        for item in self.table.get_children():
            self.table.delete(item)

        cursor = self.connection.execute(
            """
            SELECT id, name, ship_type, length, capacity
            FROM ships
            ORDER BY id
            """
        )

        for ship in cursor.fetchall():
            self.table.insert("", tk.END, values=ship)

    def delete_ship(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber loď v seznamu."
            )
            return

        ship_id = self.table.item(
            selected[0], "values"
        )[0]

        self.connection.execute(
            "DELETE FROM ships WHERE id = ?",
            (ship_id,)
        )

        self.connection.commit()
        self.load_ships()

    def close(self):
        self.connection.close()
        self.window.destroy()


def open_ships(parent):
    ShipsWindow(parent)