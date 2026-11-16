import tkinter as tk
from tkinter import ttk

from modules.ships import open_ships
from modules.buildings import open_buildings
from modules.docks import open_docks
from modules.storage_areas import open_storage_areas

# ==========================================
# PORT CITY SIMULATOR
# Hlavní aplikace
# ==========================================

root = tk.Tk()
root.title("Port City Simulator - Port Management Tool")
root.geometry("1000x750")
root.minsize(800, 600)


# Barvy aplikace

BACKGROUND = "#17232f"
PANEL = "#223342"
TEXT = "#ffffff"
ACCENT = "#36a6a0"

root.configure(bg=BACKGROUND)


# ==========================================
# HORNÍ ZÁHLAVÍ
# ==========================================

header = tk.Frame(root, bg=PANEL, height=90)
header.pack(fill="x")

title = tk.Label(
    header,
    text="PORT CITY SIMULATOR",
    font=("Arial", 22, "bold"),
    fg=TEXT,
    bg=PANEL
)
title.pack(pady=(15, 0))

subtitle = tk.Label(
    header,
    text="PORT MANAGEMENT TOOL",
    font=("Arial", 10),
    fg=ACCENT,
    bg=PANEL
)
subtitle.pack()


# ==========================================
# HLAVNÍ PRACOVNÍ PLOCHA
# ==========================================

main_frame = tk.Frame(root, bg=BACKGROUND)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)

welcome = tk.Label(
    main_frame,
    text="Vítejte v přístavním systému",
    font=("Arial", 20, "bold"),
    fg=TEXT,
    bg=BACKGROUND
)
welcome.pack(anchor="w", pady=(10, 20))

description = tk.Label(
    main_frame,
    text="Centrální správa přístavu, lodí, mol a nákladní dopravy.",
    font=("Arial", 12),
    fg=TEXT,
    bg=BACKGROUND
)
description.pack(anchor="w")


# ==========================================
# EVIDENCE LODÍ
# ==========================================

ships_button = tk.Button(
    main_frame,
    text="EVIDENCE LODÍ",
    font=("Arial", 12, "bold"),
    fg=TEXT,
    bg="#267d78",
    activebackground=ACCENT,
    activeforeground=TEXT,
    width=30,
    height=2,
    command=lambda: open_ships(root)
)

ships_button.pack(anchor="w", pady=(30, 12))


# ==========================================
# EVIDENCE BUDOV
# ==========================================

buildings_button = tk.Button(
    main_frame,
    text="EVIDENCE BUDOV",
    font=("Arial", 12, "bold"),
    fg=TEXT,
    bg="#267d78",
    activebackground=ACCENT,
    activeforeground=TEXT,
    width=30,
    height=2,
    command=lambda: open_buildings(root)
)

buildings_button.pack(anchor="w", pady=12)


# ==========================================
# EVIDENCE PŘÍSTAVNÍCH MOL
# ==========================================

docks_button = tk.Button(
    main_frame,
    text="EVIDENCE PŘÍSTAVNÍCH MOL",
    font=("Arial", 12, "bold"),
    fg=TEXT,
    bg="#267d78",
    activebackground=ACCENT,
    activeforeground=TEXT,
    width=30,
    height=2,
    command=lambda: open_docks(root)
)

docks_button.pack(anchor="w", pady=12)

# ==========================================
# EVIDENCE SKLADOVACÍCH PLOCH
# ==========================================

storage_areas_button = tk.Button(
    main_frame,
    text="EVIDENCE SKLADOVACÍCH PLOCH",
    font=("Arial", 12, "bold"),
    fg=TEXT,
    bg="#267d78",
    activebackground=ACCENT,
    activeforeground=TEXT,
    width=30,
    height=2,
    command=lambda: open_storage_areas(root)
)

storage_areas_button.pack(anchor="w", pady=12)


# ==========================================
# SPODNÍ STAVOVÝ ŘÁDEK
# ==========================================

status = tk.Label(
    root,
    text="SYSTEM ONLINE  |  PORT CITY SIMULATOR",
    font=("Arial", 9),
    fg=ACCENT,
    bg=PANEL,
    anchor="w",
    padx=15,
    pady=10
)
status.pack(side="bottom", fill="x")


# ==========================================
# SPUŠTĚNÍ APLIKACE
# ==========================================

root.mainloop()