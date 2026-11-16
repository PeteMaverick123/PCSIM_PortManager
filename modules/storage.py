
import tkinter as tk
from tkinter import ttk, messagebox

from database import Database


class StorageAreasWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Port City Simulator - Evidence skladovacích ploch")
        self.window.geometry("1250x780")
        self.window.minsize(1050, 650)

        self.db = Database()
        self.selected_id = None

        self.window.configure(bg="#20252b")

        self.create_styles()
        self.create_widgets()
        self.load_docks()
        self.load_data()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    # ======================================
    # VZHLED
    # ======================================

    def create_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#303841",
            foreground="white",
            fieldbackground="#303841",
            rowheight=27
        )

        style.configure(
            "Treeview.Heading",
            background="#45515e",
            foreground="white",
            font=("Arial", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#2675b8")]
        )

        style.configure(
            "TCombobox",
            fieldbackground="#ffffff"
        )

    # ======================================
    # HLAVNÍ ROZHRANÍ
    # ======================================

    def create_widgets(self):

        title = tk.Label(
            self.window,
            text="EVIDENCE SKLADOVACÍCH A MANIPULAČNÍCH PLOCH",
            font=("Arial", 16, "bold"),
            bg="#20252b",
            fg="white"
        )

        title.pack(pady=15)

        form_frame = tk.LabelFrame(
            self.window,
            text="Údaje o skladovací ploše",
            bg="#20252b",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )

        form_frame.pack(fill="x", padx=15, pady=5)

        self.entries = {}

        fields = [
            ("Označení plochy", "area_code"),
            ("Název", "name"),
            ("Typ plochy", "area_type"),
            ("Plocha (m²)", "area"),
            ("Kapacita", "capacity"),
            ("Aktuální obsazenost", "current_occupancy"),
            ("Měrná jednotka", "capacity_unit"),
            ("Přiřazené molo", "dock_code"),
            ("Stav", "status")
        ]

        self.area_types = [
            "Kontejnerová",
            "Otevřená skladovací",
            "Ro-Ro manipulační",
            "Univerzální nákladová",
            "Dočasná odstavná"
        ]

        self.capacity_units = [
            "TEU",
            "tun",
            "vozidel",
            "palet",
            "kusů"
        ]

        self.status_values = [
            "V provozu",
            "Odstaveno",
            "Rekonstrukce"
        ]

        for index, (label_text, key) in enumerate(fields):

            row = index // 3
            column = (index % 3) * 2

            label = tk.Label(
                form_frame,
                text=label_text,
                bg="#20252b",
                fg="white"
            )

            label.grid(
                row=row * 2,
                column=column,
                sticky="w",
                padx=8,
                pady=4
            )

            if key == "area_type":

                widget = ttk.Combobox(
                    form_frame,
                    values=self.area_types,
                    state="readonly",
                    width=25
                )

            elif key == "capacity_unit":

                widget = ttk.Combobox(
                    form_frame,
                    values=self.capacity_units,
                    state="readonly",
                    width=25
                )

            elif key == "dock_code":

                widget = ttk.Combobox(
                    form_frame,
                    state="readonly",
                    width=25
                )

            elif key == "status":

                widget = ttk.Combobox(
                    form_frame,
                    values=self.status_values,
                    state="readonly",
                    width=25
                )

            else:

                widget = tk.Entry(
                    form_frame,
                    width=28
                )

            widget.grid(
                row=row * 2 + 1,
                column=column,
                sticky="w",
                padx=8,
                pady=4
            )

            self.entries[key] = widget

        # Poznámka

        notes_label = tk.Label(
            form_frame,
            text="Poznámka",
            bg="#20252b",
            fg="white"
        )

        notes_label.grid(
            row=6,
            column=0,
            sticky="w",
            padx=8,
            pady=5
        )

        self.notes_entry = tk.Entry(
            form_frame,
            width=100
        )

        self.notes_entry.grid(
            row=6,
            column=1,
            columnspan=5,
            sticky="w",
            padx=8,
            pady=5
        )

        # Tlačítka

        button_frame = tk.Frame(
            self.window,
            bg="#20252b"
        )

        button_frame.pack(fill="x", padx=15, pady=10)

        buttons = [
            ("PŘIDAT", self.add_record),
            ("UPRAVIT", self.update_record),
            ("SMAZAT", self.delete_record),
            ("VYČISTIT", self.clear_form),
            ("OBNOVIT", self.load_data)
        ]

        for text, command in buttons:

            tk.Button(
                button_frame,
                text=text,
                command=command,
                width=14,
                bg="#45515e",
                fg="white",
                activebackground="#2675b8",
                activeforeground="white"
            ).pack(side="left", padx=5)

        # Vyhledávání

        search_frame = tk.Frame(
            self.window,
            bg="#20252b"
        )

        search_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(
            search_frame,
            text="Vyhledávání:",
            bg="#20252b",
            fg="white"
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=40
        )

        self.search_entry.pack(side="left", padx=5)

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_records
        )

        # Tabulka

        table_frame = tk.Frame(
            self.window,
            bg="#20252b"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        columns = (
            "id",
            "area_code",
            "name",
            "area_type",
            "area",
            "capacity",
            "occupancy",
            "unit",
            "dock",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "area_code": "Označení",
            "name": "Název",
            "area_type": "Typ plochy",
            "area": "Plocha m²",
            "capacity": "Kapacita",
            "occupancy": "Obsazenost",
            "unit": "Jednotka",
            "dock": "Molo",
            "status": "Stav"
        }

        widths = {
            "id": 45,
            "area_code": 115,
            "name": 180,
            "area_type": 155,
            "area": 85,
            "capacity": 85,
            "occupancy": 95,
            "unit": 75,
            "dock": 65,
            "status": 110
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_record
        )

    # ======================================
    # NAČTENÍ MOL
    # ======================================

    def load_docks(self):

        docks = self.db.fetch_all("docks")

        self.dock_codes = [
            dock["dock_code"] for dock in docks
        ]

        self.entries["dock_code"]["values"] = self.dock_codes

    # ======================================
    # NAČTENÍ DAT
    # ======================================

    def load_data(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        records = self.db.fetch_all("storage_areas")

        for record in records:

            self.tree.insert(
                "",
                "end",
                values=(
                    record["id"],
                    record["area_code"],
                    record["name"],
                    record["area_type"],
                    record["area"],
                    record["capacity"],
                    record["current_occupancy"],
                    record["capacity_unit"],
                    record["dock_code"],
                    record["status"]
                )
            )

    # ======================================
    # VYČIŠTĚNÍ FORMULÁŘE
    # ======================================

    def clear_form(self):

        for key, widget in self.entries.items():

            widget.set("") if isinstance(
                widget, ttk.Combobox
            ) else widget.delete(0, tk.END)

        self.notes_entry.delete(0, tk.END)

        self.selected_id = None

        for item in self.tree.selection():

            self.tree.selection_remove(item)

    # ======================================
    # ZÍSKÁNÍ DAT Z FORMULÁŘE
    # ======================================

    def get_form_data(self):

        data = {}

        for key, widget in self.entries.items():

            data[key] = widget.get().strip()

        data["notes"] = self.notes_entry.get().strip()

        if any(
            not data[key]
            for key in self.entries
        ):

            raise ValueError(
                "Vyplň všechna povinná pole."
            )

        try:

            data["area"] = float(data["area"])
            data["capacity"] = float(data["capacity"])
            data["current_occupancy"] = float(
                data["current_occupancy"]
            )

        except ValueError:

            raise ValueError(
                "Plocha, kapacita a obsazenost musí být čísla."
            )

        if data["area"] <= 0:

            raise ValueError(
                "Plocha musí být větší než nula."
            )

        if data["capacity"] <= 0:

            raise ValueError(
                "Kapacita musí být větší než nula."
            )

        if data["current_occupancy"] < 0:

            raise ValueError(
                "Obsazenost nesmí být záporná."
            )

        if data["current_occupancy"] > data["capacity"]:

            raise ValueError(
                "Obsazenost nesmí překročit kapacitu."
            )

        return data

    # ======================================
    # PŘIDÁNÍ ZÁZNAMU
    # ======================================

    def add_record(self):

        try:

            data = self.get_form_data()

            self.db.insert(
                "storage_areas",
                data
            )

            messagebox.showinfo(
                "Úspěch",
                "Skladovací plocha byla přidána."
            )

            self.clear_form()
            self.load_data()

        except ValueError as error:

            messagebox.showwarning(
                "Kontrola údajů",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Chyba databáze",
                str(error)
            )

    # ======================================
    # VÝBĚR ZÁZNAMU
    # ======================================

    def select_record(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_id = int(values[0])

        record = self.db.connection.execute(
            """
            SELECT * FROM storage_areas
            WHERE id = ?
            """,
            (self.selected_id,)
        ).fetchone()

        for key, widget in self.entries.items():

            value = record[key]

            if isinstance(widget, ttk.Combobox):

                widget.set(value)

            else:

                widget.delete(0, tk.END)
                widget.insert(0, value)

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, record["notes"])

    # ======================================
    # ÚPRAVA ZÁZNAMU
    # ======================================

    def update_record(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Upozornění",
                "Nejdříve vyber záznam v tabulce."
            )

            return

        try:

            data = self.get_form_data()

            self.db.update(
                "storage_areas",
                self.selected_id,
                data
            )

            messagebox.showinfo(
                "Úspěch",
                "Skladovací plocha byla upravena."
            )

            self.clear_form()
            self.load_data()

        except ValueError as error:

            messagebox.showwarning(
                "Kontrola údajů",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Chyba databáze",
                str(error)
            )

    # ======================================
    # SMAZÁNÍ ZÁZNAMU
    # ======================================

    def delete_record(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Upozornění",
                "Nejdříve vyber záznam v tabulce."
            )

            return

        confirm = messagebox.askyesno(
            "Potvrzení",
            "Opravdu chceš odstranit vybranou plochu?"
        )

        if not confirm:
            return

        try:

            self.db.delete(
                "storage_areas",
                self.selected_id
            )

            self.clear_form()
            self.load_data()

        except Exception as error:

            messagebox.showerror(
                "Chyba databáze",
                str(error)
            )

    # ======================================
    # VYHLEDÁVÁNÍ
    # ======================================

    def search_records(self, event=None):

        search_text = self.search_entry.get().lower()

        for item in self.tree.get_children():

            self.tree.delete(item)

        records = self.db.fetch_all("storage_areas")

        for record in records:

            searchable = " ".join(
                str(record[key])
                for key in record.keys()
            ).lower()

            if search_text in searchable:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        record["id"],
                        record["area_code"],
                        record["name"],
                        record["area_type"],
                        record["area"],
                        record["capacity"],
                        record["current_occupancy"],
                        record["capacity_unit"],
                        record["dock_code"],
                        record["status"]
                    )
                )

    # ======================================
    # ZAVŘENÍ OKNA
    # ======================================

    def close_window(self):

        self.db.close()
        self.window.destroy()


# ==========================================
# OTEVŘENÍ EVIDENCE
# ==========================================

def open_storage_areas(parent):

    StorageAreasWindow(parent)
