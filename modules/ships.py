
import tkinter as tk
from tkinter import ttk, messagebox

from database import Database


# ==========================================
# PORT CITY SIMULATOR
# Evidence lodí
# ==========================================

BACKGROUND = "#17232f"
PANEL = "#223342"
TEXT = "#ffffff"
ACCENT = "#36a6a0"


class ShipsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Port City Simulator - Ships")
        self.window.geometry("1100x680")
        self.window.minsize(950, 580)
        self.window.configure(bg=BACKGROUND)

        self.database = Database()
        self.selected_ship_id = None

        self.create_interface()
        self.load_ships()

        self.window.protocol("WM_DELETE_WINDOW", self.close)

    # ======================================
    # GRAFICKÉ ROZHRANÍ
    # ======================================

    def create_interface(self):

        header = tk.Frame(
            self.window,
            bg=PANEL,
            height=75
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="SHIP REGISTRY",
            font=("Arial", 21, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(pady=20)

        # FORMULÁŘ

        form = tk.LabelFrame(
            self.window,
            text=" Údaje o lodi ",
            font=("Arial", 11, "bold"),
            fg=ACCENT,
            bg=BACKGROUND,
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=20, pady=15)

        tk.Label(
            form,
            text="Název lodi:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.name_entry = tk.Entry(form, width=23)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(
            form,
            text="Typ lodě:",
            fg=TEXT,
            bg=BACKGROUND
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
            form,
            text="Délka (m):",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=2, sticky="w", padx=5)

        self.length_entry = tk.Entry(form, width=15)
        self.length_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(
            form,
            text="Kapacita (t):",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=3, sticky="w", padx=5)

        self.capacity_entry = tk.Entry(form, width=15)
        self.capacity_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(
            form,
            text="Ponor (m):",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=4, sticky="w", padx=5)

        self.draft_entry = tk.Entry(form, width=15)
        self.draft_entry.grid(row=1, column=4, padx=5, pady=5)

        # OVLÁDACÍ TLAČÍTKA

        buttons = tk.Frame(form, bg=BACKGROUND)
        buttons.grid(
            row=2,
            column=0,
            columnspan=5,
            pady=12
        )

        ttk.Button(
            buttons,
            text="Přidat loď",
            command=self.add_ship
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Načíst vybranou",
            command=self.select_ship
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Uložit změny",
            command=self.update_ship
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Vyčistit formulář",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # VYHLEDÁVÁNÍ

        search_frame = tk.Frame(
            self.window,
            bg=BACKGROUND
        )
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            search_frame,
            text="Vyhledávání:",
            fg=TEXT,
            bg=BACKGROUND
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )
        self.search_entry.pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Hledat",
            command=self.search_ships
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Zobrazit vše",
            command=self.load_ships
        ).pack(side="left", padx=5)

        # TABULKA

        table_frame = tk.Frame(
            self.window,
            bg=BACKGROUND
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "id",
            "name",
            "type",
            "length",
            "capacity",
            "draft"
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
            "capacity": "Kapacita (t)",
            "draft": "Ponor (m)"
        }

        widths = {
            "id": 50,
            "name": 220,
            "type": 160,
            "length": 120,
            "capacity": 140,
            "draft": 120
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

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # SPODNÍ OVLÁDÁNÍ

        ttk.Button(
            self.window,
            text="Odstranit vybranou položku",
            command=self.delete_ship
        ).pack(pady=10)

    # ======================================
    # NAČTENÍ LODÍ
    # ======================================

    def load_ships(self):

        for item in self.table.get_children():
            self.table.delete(item)

        ships = self.database.fetch_all("ships")

        for ship in ships:

            draft_value = (
                ship["draft"] if ship["draft"] > 0 else "Nezadáno"
            )

            self.table.insert(
                "",
                tk.END,
                values=(
                    ship["id"],
                    ship["name"],
                    ship["ship_type"],
                    ship["length"],
                    ship["capacity"],
                    draft_value
                )
            )

    # ======================================
    # PŘIDÁNÍ LODI
    # ======================================

    def add_ship(self):

        data = self.get_form_data()

        if data is None:
            return

        self.database.insert("ships", data)

        self.clear_form()
        self.load_ships()

        messagebox.showinfo(
            "Evidence lodí",
            "Loď byla úspěšně přidána."
        )

    # ======================================
    # ZÍSKÁNÍ ÚDAJŮ Z FORMULÁŘE
    # ======================================

    def get_form_data(self):

        name = self.name_entry.get().strip()
        ship_type = self.type_box.get()

        try:

            length = float(
                self.length_entry.get().replace(",", ".")
            )

            capacity = float(
                self.capacity_entry.get().replace(",", ".")
            )

            draft = float(
                self.draft_entry.get().replace(",", ".")
            )

        except ValueError:

            messagebox.showerror(
                "Chybný údaj",
                "Délka, kapacita a ponor musí být čísla."
            )

            return None

        if (
            not name
            or length <= 0
            or capacity <= 0
            or draft <= 0
        ):

            messagebox.showerror(
                "Chybný údaj",
                "Vyplň název a zadej kladné hodnoty délky, kapacity a ponoru."
            )

            return None

        if not ship_type:

            messagebox.showerror(
                "Chybný údaj",
                "Vyber typ lodě."
            )

            return None

        return {
            "name": name,
            "ship_type": ship_type,
            "length": length,
            "capacity": capacity,
            "draft": draft
        }

    # ======================================
    # VÝBĚR LODI PRO ÚPRAVU
    # ======================================

    def select_ship(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber loď v seznamu."
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        self.selected_ship_id = int(values[0])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.type_box.set(values[2])

        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, values[3])

        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, values[4])

        self.draft_entry.delete(0, tk.END)

        if values[5] != "Nezadáno":
            self.draft_entry.insert(0, values[5])

    # ======================================
    # ÚPRAVA LODI
    # ======================================

    def update_ship(self):

        if self.selected_ship_id is None:

            messagebox.showinfo(
                "Úprava záznamu",
                "Nejdříve vyber loď a klikni na Načíst vybranou."
            )

            return

        data = self.get_form_data()

        if data is None:
            return

        self.database.update(
            "ships",
            self.selected_ship_id,
            data
        )

        self.clear_form()
        self.load_ships()

        messagebox.showinfo(
            "Evidence lodí",
            "Údaje o lodi byly aktualizovány."
        )

    # ======================================
    # VYHLEDÁVÁNÍ
    # ======================================

    def search_ships(self):

        search_text = self.search_entry.get().strip().lower()

        for item in self.table.get_children():
            self.table.delete(item)

        ships = self.database.fetch_all("ships")

        for ship in ships:

            searchable_values = (
                str(ship["id"]),
                ship["name"],
                ship["ship_type"],
                str(ship["length"]),
                str(ship["capacity"]),
                str(ship["draft"])
            )

            if any(
                search_text in value.lower()
                for value in searchable_values
            ):

                draft_value = (
                    ship["draft"] if ship["draft"] > 0 else "Nezadáno"
                )

                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        ship["id"],
                        ship["name"],
                        ship["ship_type"],
                        ship["length"],
                        ship["capacity"],
                        draft_value
                    )
                )

    # ======================================
    # ODSTRANĚNÍ LODI
    # ======================================

    def delete_ship(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber položku v seznamu."
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        ship_id = int(values[0])
        ship_name = values[1]

        confirmation = messagebox.askyesno(
            "Potvrzení odstranění",
            f"Opravdu chceš odstranit loď {ship_name}?"
        )

        if not confirmation:
            return

        self.database.delete(
            "ships",
            ship_id
        )

        self.clear_form()
        self.load_ships()

    # ======================================
    # VYČIŠTĚNÍ FORMULÁŘE
    # ======================================

    def clear_form(self):

        self.name_entry.delete(0, tk.END)
        self.type_box.current(0)
        self.length_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.draft_entry.delete(0, tk.END)

        self.selected_ship_id = None

    # ======================================
    # ZAVŘENÍ OKNA
    # ======================================

    def close(self):

        self.database.close()
        self.window.destroy()


def open_ships(parent):

    ShipsWindow(parent)
