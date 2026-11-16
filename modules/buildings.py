import tkinter as tk
from tkinter import ttk, messagebox

from database import Database


# ==========================================
# PORT CITY SIMULATOR
# Evidence přístavních budov
# ==========================================

BACKGROUND = "#17232f"
PANEL = "#223342"
TEXT = "#ffffff"
ACCENT = "#36a6a0"


class BuildingsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Port City Simulator - Buildings")
        self.window.geometry("1100x700")
        self.window.minsize(900, 600)
        self.window.configure(bg=BACKGROUND)

        self.database = Database()
        self.selected_building_id = None

        self.create_interface()
        self.load_buildings()

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
            text="PORT BUILDINGS REGISTRY",
            font=("Arial", 21, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(pady=20)

        # FORMULÁŘ

        form = tk.LabelFrame(
            self.window,
            text=" Údaje o objektu ",
            font=("Arial", 11, "bold"),
            fg=ACCENT,
            bg=BACKGROUND,
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=20, pady=15)

        tk.Label(
            form,
            text="Název objektu:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.name_entry = tk.Entry(form, width=24)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(
            form,
            text="Typ objektu:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.type_box = ttk.Combobox(
            form,
            values=[
                "Administrativní budova",
                "Sklad",
                "Servisní dílna",
                "Celní budova",
                "Technické zázemí",
                "Jiné"
            ],
            state="normal",
            width=23
        )
        self.type_box.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Plocha (m²):",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=2, sticky="w", padx=5)

        self.area_entry = tk.Entry(form, width=15)
        self.area_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(
            form,
            text="Stav objektu:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=0, column=3, sticky="w", padx=5)

        self.status_box = ttk.Combobox(
            form,
            values=[
                "V provozu",
                "Odstaveno",
                "Ve výstavbě"
            ],
            state="readonly",
            width=17
        )
        self.status_box.grid(row=1, column=3, padx=5, pady=5)
        self.status_box.current(0)

        tk.Label(
            form,
            text="Rok výstavby:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=2, column=0, sticky="w", padx=5, pady=(10, 0))

        self.year_entry = tk.Entry(form, width=24)
        self.year_entry.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(
            form,
            text="Poznámka:",
            fg=TEXT,
            bg=BACKGROUND
        ).grid(row=2, column=1, sticky="w", padx=5, pady=(10, 0))

        self.notes_entry = tk.Entry(form, width=55)
        self.notes_entry.grid(
            row=3,
            column=1,
            columnspan=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # OVLÁDACÍ TLAČÍTKA

        buttons = tk.Frame(form, bg=BACKGROUND)
        buttons.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=12
        )

        ttk.Button(
            buttons,
            text="Přidat objekt",
            command=self.add_building
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Načíst vybraný",
            command=self.select_building
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Uložit změny",
            command=self.update_building
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
            command=self.search_buildings
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Zobrazit vše",
            command=self.load_buildings
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
            "area",
            "status",
            "year",
            "notes"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Název objektu",
            "type": "Typ",
            "area": "Plocha (m²)",
            "status": "Stav",
            "year": "Rok výstavby",
            "notes": "Poznámka"
        }

        widths = {
            "id": 45,
            "name": 180,
            "type": 170,
            "area": 100,
            "status": 110,
            "year": 100,
            "notes": 220
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

        # ODSTRANĚNÍ

        ttk.Button(
            self.window,
            text="Odstranit vybranou položku",
            command=self.delete_building
        ).pack(pady=10)

    # ======================================
    # ZÍSKÁNÍ ÚDAJŮ Z FORMULÁŘE
    # ======================================

    def get_form_data(self):

        name = self.name_entry.get().strip()
        building_type = self.type_box.get().strip()
        status = self.status_box.get()

        if not name or not building_type or not status:

            messagebox.showerror(
                "Chybný údaj",
                "Vyplň název, typ a stav objektu."
            )
            return None

        try:

            area = float(
                self.area_entry.get().replace(",", ".")
            )

            if area <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Chybný údaj",
                "Plocha musí být kladné číslo."
            )
            return None

        year_text = self.year_entry.get().strip()

        if year_text:

            try:
                year = int(year_text)

                if year < 1 or year > 9999:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Chybný údaj",
                    "Rok výstavby musí být platný rok."
                )
                return None

        else:
            year = None

        return {
            "name": name,
            "building_type": building_type,
            "area": area,
            "status": status,
            "construction_year": year,
            "notes": self.notes_entry.get().strip()
        }

    # ======================================
    # NAČTENÍ OBJEKTŮ
    # ======================================

    def load_buildings(self):

        self.search_entry.delete(0, tk.END)

        for item in self.table.get_children():
            self.table.delete(item)

        buildings = self.database.fetch_all("buildings")

        for building in buildings:

            self.table.insert(
                "",
                tk.END,
                values=(
                    building["id"],
                    building["name"],
                    building["building_type"],
                    building["area"],
                    building["status"],
                    building["construction_year"] or "",
                    building["notes"]
                )
            )

    # ======================================
    # PŘIDÁNÍ OBJEKTU
    # ======================================

    def add_building(self):

        data = self.get_form_data()

        if data is None:
            return

        self.database.insert("buildings", data)

        self.clear_form()
        self.load_buildings()

        messagebox.showinfo(
            "Evidence budov",
            "Objekt byl úspěšně přidán."
        )

    # ======================================
    # VÝBĚR OBJEKTU PRO ÚPRAVU
    # ======================================

    def select_building(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber objekt v seznamu."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        self.selected_building_id = int(values[0])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.type_box.set(values[2])

        self.area_entry.delete(0, tk.END)
        self.area_entry.insert(0, values[3])

        self.status_box.set(values[4])

        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, values[5])

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, values[6])

    # ======================================
    # ÚPRAVA OBJEKTU
    # ======================================

    def update_building(self):

        if self.selected_building_id is None:

            messagebox.showinfo(
                "Úprava záznamu",
                "Nejdříve načti vybraný objekt."
            )
            return

        data = self.get_form_data()

        if data is None:
            return

        self.database.update(
            "buildings",
            self.selected_building_id,
            data
        )

        self.clear_form()
        self.load_buildings()

        messagebox.showinfo(
            "Evidence budov",
            "Údaje o objektu byly aktualizovány."
        )

    # ======================================
    # VYHLEDÁVÁNÍ
    # ======================================

    def search_buildings(self):

        search_text = self.search_entry.get().strip().lower()

        for item in self.table.get_children():
            self.table.delete(item)

        buildings = self.database.fetch_all("buildings")

        for building in buildings:

            values = (
                str(building["id"]),
                building["name"],
                building["building_type"],
                str(building["area"]),
                building["status"],
                str(building["construction_year"] or ""),
                building["notes"]
            )

            if any(
                search_text in str(value).lower()
                for value in values
            ):

                self.table.insert(
                    "",
                    tk.END,
                    values=values
                )

    # ======================================
    # ODSTRANĚNÍ OBJEKTU
    # ======================================

    def delete_building(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Výběr",
                "Nejdříve vyber objekt v seznamu."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        building_id = int(values[0])
        building_name = values[1]

        confirmation = messagebox.askyesno(
            "Potvrzení odstranění",
            f"Opravdu chceš odstranit objekt {building_name}?"
        )

        if not confirmation:
            return

        self.database.delete(
            "buildings",
            building_id
        )

        self.clear_form()
        self.load_buildings()

    # ======================================
    # VYČIŠTĚNÍ FORMULÁŘE
    # ======================================

    def clear_form(self):

        self.name_entry.delete(0, tk.END)
        self.type_box.set("")
        self.area_entry.delete(0, tk.END)
        self.status_box.current(0)
        self.year_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        self.selected_building_id = None

    # ======================================
    # ZAVŘENÍ OKNA
    # ======================================

    def close(self):

        self.database.close()
        self.window.destroy()


def open_buildings(parent):

    BuildingsWindow(parent)