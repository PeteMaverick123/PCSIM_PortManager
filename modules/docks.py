import tkinter as tk
from tkinter import ttk, messagebox

from database import Database


# ==========================================
# PORT CITY SIMULATOR
# Evidence přístavních mol
# ==========================================

BACKGROUND = "#17232f"
PANEL = "#223342"
TEXT = "#ffffff"
ACCENT = "#36a6a0"


class DocksWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Port City Simulator - Docks")
        self.window.geometry("1250x780")
        self.window.minsize(1050, 650)
        self.window.configure(bg=BACKGROUND)

        self.database = Database()
        self.selected_dock_id = None

        self.create_interface()
        self.load_docks()

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
            text="PORT DOCKS REGISTRY",
            font=("Arial", 21, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(pady=20)

        # FORMULÁŘ

        form = tk.LabelFrame(
            self.window,
            text=" Údaje o přístavním molu ",
            font=("Arial", 11, "bold"),
            fg=ACCENT,
            bg=BACKGROUND,
            padx=15,
            pady=12
        )
        form.pack(fill="x", padx=20, pady=12)

        # První řádek

        labels = [
            "Označení mola:",
            "Název mola:",
            "Délka (m):",
            "Hloubka (m):",
            "Max. ponor (m):"
        ]

        for column, label_text in enumerate(labels):
            tk.Label(
                form,
                text=label_text,
                fg=TEXT,
                bg=BACKGROUND
            ).grid(
                row=0,
                column=column,
                sticky="w",
                padx=5
            )

        self.code_entry = tk.Entry(form, width=13)
        self.code_entry.grid(row=1, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(form, width=25)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.length_entry = tk.Entry(form, width=13)
        self.length_entry.grid(row=1, column=2, padx=5, pady=5)

        self.depth_entry = tk.Entry(form, width=13)
        self.depth_entry.grid(row=1, column=3, padx=5, pady=5)

        self.max_draft_entry = tk.Entry(form, width=13)
        self.max_draft_entry.grid(row=1, column=4, padx=5, pady=5)

        # Druhý řádek

        second_labels = [
            "Max. délka lodě (m):",
            "Kapacita lodí:",
            "Typ nákladu:",
            "Stav mola:",
            "Železniční napojení:"
        ]

        for column, label_text in enumerate(second_labels):
            tk.Label(
                form,
                text=label_text,
                fg=TEXT,
                bg=BACKGROUND
            ).grid(
                row=2,
                column=column,
                sticky="w",
                padx=5,
                pady=(10, 0)
            )

        self.max_ship_length_entry = tk.Entry(
            form,
            width=13
        )
        self.max_ship_length_entry.grid(
            row=3,
            column=0,
            padx=5,
            pady=5
        )

        self.ship_capacity_entry = tk.Entry(
            form,
            width=13
        )
        self.ship_capacity_entry.grid(
            row=3,
            column=1,
            padx=5,
            pady=5
        )

        self.cargo_box = ttk.Combobox(
            form,
            values=[
                "General Cargo",
                "Kontejnery",
                "Kapaliny a ropné produkty",
                "Ro-Ro náklad",
                "Osobní doprava",
                "Sypký náklad",
                "Jiné"
            ],
            state="normal",
            width=23
        )
        self.cargo_box.grid(
            row=3,
            column=2,
            padx=5,
            pady=5
        )

        self.status_box = ttk.Combobox(
            form,
            values=[
                "V provozu",
                "Odstaveno",
                "Ve výstavbě"
            ],
            state="readonly",
            width=15
        )
        self.status_box.grid(
            row=3,
            column=3,
            padx=5,
            pady=5
        )
        self.status_box.current(0)

        self.rail_box = ttk.Combobox(
            form,
            values=["Ano", "Ne"],
            state="readonly",
            width=10
        )
        self.rail_box.grid(
            row=3,
            column=4,
            padx=5,
            pady=5
        )
        self.rail_box.current(1)

        # Poznámka

        tk.Label(
            form,
            text="Poznámka:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=5,
            pady=(8, 0)
        )

        self.notes_entry = tk.Entry(form, width=90)
        self.notes_entry.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky="w",
            padx=5,
            pady=5
        )

        # TLAČÍTKA

        buttons = tk.Frame(form, bg=BACKGROUND)
        buttons.grid(
            row=6,
            column=0,
            columnspan=5,
            pady=12
        )

        ttk.Button(
            buttons,
            text="Přidat molo",
            command=self.add_dock
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Načíst vybrané",
            command=self.select_dock
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Uložit změny",
            command=self.update_dock
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
            command=self.search_docks
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Zobrazit vše",
            command=self.load_docks
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
            "code",
            "name",
            "length",
            "depth",
            "max_draft",
            "max_ship_length",
            "ship_capacity",
            "cargo_type",
            "status",
            "rail"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "code": "Označení",
            "name": "Název mola",
            "length": "Délka (m)",
            "depth": "Hloubka (m)",
            "max_draft": "Max. ponor",
            "max_ship_length": "Max. délka lodě",
            "ship_capacity": "Kapacita",
            "cargo_type": "Typ nákladu",
            "status": "Stav",
            "rail": "Železnice"
        }

        widths = {
            "id": 45,
            "code": 75,
            "name": 190,
            "length": 85,
            "depth": 85,
            "max_draft": 90,
            "max_ship_length": 115,
            "ship_capacity": 75,
            "cargo_type": 180,
            "status": 105,
            "rail": 85
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

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # ODSTRANĚNÍ

        ttk.Button(
            self.window,
            text="Odstranit vybrané molo",
            command=self.delete_dock
        ).pack(pady=10)

    # ======================================
    # PŘÍPRAVA ÚDAJŮ
    # ======================================

    def get_form_data(self):

        code = self.code_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        cargo_type = self.cargo_box.get().strip()
        status = self.status_box.get()
        rail_connection = (
            1 if self.rail_box.get() == "Ano" else 0
        )
        notes = self.notes_entry.get().strip()

        try:

            length = float(
                self.length_entry.get().replace(",", ".")
            )

            depth = float(
                self.depth_entry.get().replace(",", ".")
            )

            max_draft = float(
                self.max_draft_entry.get().replace(",", ".")
            )

            max_ship_length = float(
                self.max_ship_length_entry.get().replace(",", ".")
            )

            ship_capacity = int(
                self.ship_capacity_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Chybný údaj",
                "Rozměry musí být čísla a kapacita celé číslo."
            )

            return None

        if (
            not code
            or not name
            or not cargo_type
            or not status
            or length <= 0
            or depth <= 0
            or max_draft <= 0
            or max_ship_length <= 0
            or ship_capacity <= 0
        ):

            messagebox.showerror(
                "Chybný údaj",
                "Vyplň všechna povinná pole kladnými hodnotami."
            )

            return None

        if max_draft >= depth:

            messagebox.showerror(
                "Chybný údaj",
                "Maximální ponor musí být menší než hloubka vody."
            )

            return None

        if max_ship_length > length:

            messagebox.showerror(
                "Chybný údaj",
                "Maximální délka lodě nemůže být větší než délka mola."
            )

            return None

        return {
            "dock_code": code,
            "name": name,
            "length": length,
            "depth": depth,
            "max_draft": max_draft,
            "max_ship_length": max_ship_length,
            "ship_capacity": ship_capacity,
            "cargo_type": cargo_type,
            "status": status,
            "rail_connection": rail_connection,
            "notes": notes
        }

    # ======================================
    # VLOŽENÍ ŘÁDKU DO TABULKY
    # ======================================

    def insert_dock_row(self, dock):

        self.table.insert(
            "",
            tk.END,
            values=(
                dock["id"],
                dock["dock_code"],
                dock["name"],
                dock["length"],
                dock["depth"],
                dock["max_draft"],
                dock["max_ship_length"],
                dock["ship_capacity"],
                dock["cargo_type"],
                dock["status"],
                "Ano" if dock["rail_connection"] else "Ne"
            )
        )

    # ======================================
    # NAČTENÍ MOL
    # ======================================

    def load_docks(self):

        for item in self.table.get_children():
            self.table.delete(item)

        docks = self.database.fetch_all("docks")

        for dock in docks:
            self.insert_dock_row(dock)

        self.search_entry.delete(0, tk.END)

    # ======================================
    # PŘIDÁNÍ MOLA
    # ======================================

    def add_dock(self):

        data = self.get_form_data()

        if data is None:
            return

        try:
            self.database.insert("docks", data)

        except Exception as error:

            messagebox.showerror(
                "Chyba při ukládání",
                f"Molo se nepodařilo přidat.\n\n{error}"
            )
            return

        self.clear_form()
        self.load_docks()

        messagebox.showinfo(
            "Evidence mol",
            "Molo bylo úspěšně přidáno."
        )

    # ======================================
    # VÝBĚR MOLA PRO ÚPRAVU
    # ======================================

    def select_dock(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber molo v seznamu."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        self.selected_dock_id = int(values[0])

        dock = next(
            (
                item for item in self.database.fetch_all("docks")
                if item["id"] == self.selected_dock_id
            ),
            None
        )

        if dock is None:
            return

        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, dock["dock_code"])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, dock["name"])

        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, dock["length"])

        self.depth_entry.delete(0, tk.END)
        self.depth_entry.insert(0, dock["depth"])

        self.max_draft_entry.delete(0, tk.END)
        self.max_draft_entry.insert(0, dock["max_draft"])

        self.max_ship_length_entry.delete(0, tk.END)
        self.max_ship_length_entry.insert(
            0, dock["max_ship_length"]
        )

        self.ship_capacity_entry.delete(0, tk.END)
        self.ship_capacity_entry.insert(
            0, dock["ship_capacity"]
        )

        self.cargo_box.set(dock["cargo_type"])
        self.status_box.set(dock["status"])

        self.rail_box.set(
            "Ano" if dock["rail_connection"] else "Ne"
        )

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, dock["notes"] or "")

    # ======================================
    # ÚPRAVA MOLA
    # ======================================

    def update_dock(self):

        if self.selected_dock_id is None:

            messagebox.showinfo(
                "Úprava záznamu",
                "Nejdříve vyber molo a klikni na Načíst vybrané."
            )
            return

        data = self.get_form_data()

        if data is None:
            return

        try:
            self.database.update(
                "docks",
                self.selected_dock_id,
                data
            )

        except Exception as error:

            messagebox.showerror(
                "Chyba při ukládání",
                f"Změny se nepodařilo uložit.\n\n{error}"
            )
            return

        self.clear_form()
        self.load_docks()

        messagebox.showinfo(
            "Evidence mol",
            "Údaje o molu byly aktualizovány."
        )

    # ======================================
    # VYHLEDÁVÁNÍ
    # ======================================

    def search_docks(self):

        search_text = (
            self.search_entry.get().strip().lower()
        )

        for item in self.table.get_children():
            self.table.delete(item)

        docks = self.database.fetch_all("docks")

        for dock in docks:

            searchable_values = (
                str(dock["id"]),
                dock["dock_code"],
                dock["name"],
                str(dock["length"]),
                str(dock["depth"]),
                str(dock["max_draft"]),
                str(dock["max_ship_length"]),
                str(dock["ship_capacity"]),
                dock["cargo_type"],
                dock["status"],
                "ano" if dock["rail_connection"] else "ne",
                dock["notes"] or ""
            )

            if any(
                search_text in value.lower()
                for value in searchable_values
            ):
                self.insert_dock_row(dock)

    # ======================================
    # ODSTRANĚNÍ MOLA
    # ======================================

    def delete_dock(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber molo v seznamu."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        dock_id = int(values[0])
        dock_name = values[2]

        confirmation = messagebox.askyesno(
            "Potvrzení odstranění",
            f"Opravdu chceš odstranit molo {dock_name}?"
        )

        if not confirmation:
            return

        self.database.delete(
            "docks",
            dock_id
        )

        self.clear_form()
        self.load_docks()

    # ======================================
    # VYČIŠTĚNÍ FORMULÁŘE
    # ======================================

    def clear_form(self):

        self.code_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.length_entry.delete(0, tk.END)
        self.depth_entry.delete(0, tk.END)
        self.max_draft_entry.delete(0, tk.END)
        self.max_ship_length_entry.delete(0, tk.END)
        self.ship_capacity_entry.delete(0, tk.END)
        self.cargo_box.set("")
        self.status_box.current(0)
        self.rail_box.current(1)
        self.notes_entry.delete(0, tk.END)

        self.selected_dock_id = None

    # ======================================
    # ZAVŘENÍ OKNA
    # ======================================

    def close(self):

        self.database.close()
        self.window.destroy()


def open_docks(parent):

    DocksWindow(parent)