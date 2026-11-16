
import sqlite3
from pathlib import Path


# ==========================================
# PORT CITY SIMULATOR
# Centrální databázový systém
# ==========================================

DB_FILE = Path(__file__).with_name("port_city.db")


class Database:

    TABLE_COLUMNS = {
        "ships": {
            "name",
            "ship_type",
            "length",
            "capacity",
            "draft"
        },
        "buildings": {
            "name",
            "building_type",
            "area",
            "status",
            "construction_year",
            "notes"
        },
        "docks": {
            "dock_code",
            "name",
            "length",
            "depth",
            "max_draft",
            "max_ship_length",
            "ship_capacity",
            "cargo_type",
            "status",
            "rail_connection",
            "notes"
        },
        "storage_areas": {
            "area_code",
            "name",
            "area_type",
            "area",
            "capacity",
            "current_occupancy",
            "capacity_unit",
            "dock_code",
            "status",
            "notes"
        }
    }

    def __init__(self):

        self.connection = sqlite3.connect(DB_FILE)
        self.connection.row_factory = sqlite3.Row

        # Aktivace kontroly cizích klíčů
        self.connection.execute("PRAGMA foreign_keys = ON")

        self.create_tables()
        self.migrate_database()
        self.seed_docks()
        self.seed_storage_areas()

    # ======================================
    # VYTVOŘENÍ DATABÁZOVÝCH TABULEK
    # ======================================

    def create_tables(self):

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS ships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ship_type TEXT NOT NULL,
                length REAL NOT NULL,
                capacity REAL NOT NULL,
                draft REAL NOT NULL DEFAULT 0
            )
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS buildings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                building_type TEXT NOT NULL,
                area REAL NOT NULL CHECK(area > 0),
                status TEXT NOT NULL,
                construction_year INTEGER,
                notes TEXT DEFAULT ''
            )
        """)

        # Evidence přístavních mol

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS docks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dock_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                length REAL NOT NULL CHECK(length > 0),
                depth REAL NOT NULL CHECK(depth > 0),
                max_draft REAL NOT NULL CHECK(max_draft > 0),
                max_ship_length REAL NOT NULL CHECK(max_ship_length > 0),
                ship_capacity INTEGER NOT NULL CHECK(ship_capacity > 0),
                cargo_type TEXT NOT NULL,
                status TEXT NOT NULL,
                rail_connection INTEGER NOT NULL DEFAULT 0,
                notes TEXT DEFAULT ''
            )
        """)

        # Evidence skladovacích a manipulačních ploch

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS storage_areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                area_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                area_type TEXT NOT NULL,

                area REAL NOT NULL CHECK(area > 0),

                capacity REAL NOT NULL CHECK(capacity > 0),

                current_occupancy REAL NOT NULL DEFAULT 0
                    CHECK(current_occupancy >= 0),

                capacity_unit TEXT NOT NULL,

                dock_code TEXT NOT NULL,

                status TEXT NOT NULL,

                notes TEXT DEFAULT '',

                FOREIGN KEY (dock_code)
                    REFERENCES docks(dock_code)
                    ON DELETE RESTRICT,

                CHECK(current_occupancy <= capacity)
            )
        """)

        self.connection.commit()

    # ======================================
    # AKTUALIZACE DATABÁZE
    # ======================================

    def migrate_database(self):

        cursor = self.connection.execute(
            "PRAGMA table_info(ships)"
        )

        existing_columns = {
            row["name"] for row in cursor.fetchall()
        }

        if "draft" not in existing_columns:

            self.connection.execute("""
                ALTER TABLE ships
                ADD COLUMN draft REAL NOT NULL DEFAULT 0
            """)

            self.connection.commit()

    # ======================================
    # DEMONSTRAČNÍ DATA MOL
    # ======================================

    def seed_docks(self):

        sample_docks = [
            (
                "A1",
                "General Cargo Terminal",
                350,
                13,
                11.5,
                300,
                2,
                "General Cargo",
                "V provozu",
                1,
                "Univerzální nákladní molo."
            ),
            (
                "A2",
                "Container Terminal",
                450,
                15,
                13.5,
                400,
                2,
                "Kontejnery",
                "V provozu",
                1,
                "Specializované kontejnerové molo."
            ),
            (
                "B1",
                "Oil Terminal",
                300,
                14,
                12.5,
                250,
                1,
                "Kapaliny a ropné produkty",
                "V provozu",
                0,
                "Terminál pro přečerpávání kapalného nákladu."
            ),
            (
                "B2",
                "Ro-Ro Terminal",
                280,
                10,
                8.5,
                240,
                1,
                "Ro-Ro náklad",
                "V provozu",
                1,
                "Molo pro lodě s nájezdem vozidel."
            ),
            (
                "C1",
                "Passenger Terminal",
                220,
                9,
                7.5,
                200,
                2,
                "Osobní doprava",
                "V provozu",
                0,
                "Terminál pro osobní lodě a cestující."
            )
        ]

        self.connection.executemany("""
            INSERT OR IGNORE INTO docks (
                dock_code,
                name,
                length,
                depth,
                max_draft,
                max_ship_length,
                ship_capacity,
                cargo_type,
                status,
                rail_connection,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_docks)

        self.connection.commit()

    # ======================================
    # DEMONSTRAČNÍ DATA SKLADOVACÍCH PLOCH
    # ======================================

    def seed_storage_areas(self):

        sample_areas = [
            (
                "CY-A1-01",
                "General Cargo Yard",
                "Univerzální nákladová",
                8000,
                300,
                75,
                "tun",
                "A1",
                "V provozu",
                "Otevřená plocha pro kusový a paletový náklad."
            ),
            (
                "CY-A2-01",
                "Main Container Yard",
                "Kontejnerová",
                15000,
                500,
                180,
                "TEU",
                "A2",
                "V provozu",
                "Hlavní kontejnerová skladovací plocha."
            ),
            (
                "CY-A2-02",
                "Secondary Container Yard",
                "Kontejnerová",
                9000,
                300,
                90,
                "TEU",
                "A2",
                "V provozu",
                "Vedlejší plocha pro kontejnery."
            ),
            (
                "RY-B2-01",
                "Ro-Ro Storage Area",
                "Ro-Ro manipulační",
                12000,
                250,
                65,
                "vozidel",
                "B2",
                "V provozu",
                "Odstavná plocha pro vozidla a Ro-Ro náklad."
            ),
            (
                "YA-B1-01",
                "Industrial Cargo Yard",
                "Otevřená skladovací",
                6000,
                400,
                100,
                "tun",
                "B1",
                "V provozu",
                "Modelová plocha pro průmyslový náklad."
            )
        ]

        self.connection.executemany("""
            INSERT OR IGNORE INTO storage_areas (
                area_code,
                name,
                area_type,
                area,
                capacity,
                current_occupancy,
                capacity_unit,
                dock_code,
                status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_areas)

        self.connection.commit()

    # ======================================
    # KONTROLA TABULKY A SLOUPCŮ
    # ======================================

    def validate_data(self, table, data=None):

        if table not in self.TABLE_COLUMNS:
            raise ValueError("Neznámá databázová tabulka.")

        if data is not None:

            if not data:
                raise ValueError("Nebyla zadána žádná data.")

            if not set(data.keys()).issubset(
                self.TABLE_COLUMNS[table]
            ):
                raise ValueError("Neplatný databázový sloupec.")

    # ======================================
    # NAČÍTÁNÍ ZÁZNAMŮ
    # ======================================

    def fetch_all(self, table):

        self.validate_data(table)

        cursor = self.connection.execute(
            f"SELECT * FROM {table} ORDER BY id"
        )

        return cursor.fetchall()

    # ======================================
    # PŘIDÁNÍ ZÁZNAMU
    # ======================================

    def insert(self, table, data):

        self.validate_data(table, data)

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)

        query = (
            f"INSERT INTO {table} "
            f"({columns}) VALUES ({placeholders})"
        )

        self.connection.execute(
            query,
            tuple(data.values())
        )

        self.connection.commit()

    # ======================================
    # ÚPRAVA ZÁZNAMU
    # ======================================

    def update(self, table, record_id, data):

        self.validate_data(table, data)

        assignments = ", ".join(
            f"{column} = ?" for column in data
        )

        query = (
            f"UPDATE {table} SET {assignments} "
            "WHERE id = ?"
        )

        self.connection.execute(
            query,
            (*data.values(), record_id)
        )

        self.connection.commit()

    # ======================================
    # ODSTRANĚNÍ ZÁZNAMU
    # ======================================

    def delete(self, table, record_id):

        self.validate_data(table)

        self.connection.execute(
            f"DELETE FROM {table} WHERE id = ?",
            (record_id,)
        )

        self.connection.commit()

    # ======================================
    # ZAVŘENÍ DATABÁZE
    # ======================================

    def close(self):

        self.connection.close()
