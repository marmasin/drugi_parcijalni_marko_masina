import sqlite3

class Database:
    def __init__(self, db_name="db.sqlite3"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row # Omogućava pristup stupcima po imenu
        self.cursor = self.conn.cursor()
        print(f"Povezan s bazom podataka: {self.db_name}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(f"Prekinuta veza s bazom podataka: {self.db_name}")

    def execute_query(self, query, params=()):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Greška pri izvršavanju upita: {e}")
            return None

    def fetch_query(self, query, params=()):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Greška pri dohvaćanju podataka: {e}")
            return []

    def fetch_one_query(self, query, params=()):
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Greška pri dohvaćanju jednog podatka: {e}")
            return None

    def create_tables(self):
        if not self.conn:
            self.connect()

        # Tablica za kupce
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            vat_id TEXT
        )
        """)

        # Tablica za proizvode
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
        """)

        # Tablica za ponude
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            offer_date TEXT NOT NULL,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
        """)
        # Dodatna tablica za stavke ponude (povezuje proizvode s ponudama - many-to-many)
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS offer_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL, -- Cijena proizvoda u trenutku izrade ponude
            FOREIGN KEY (offer_id) REFERENCES offers (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """)
        print("Tablice uspješno kreirane ili već postoje.")

# Primjer inicijalizacije baze i kreiranja tablica pri pokretanju
if __name__ == '__main__':
    db = Database()
    db.connect()
    db.create_tables()
    db.disconnect()