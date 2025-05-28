class Customer:
    def __init__(self, db, customer_id=None, name=None, email=None, vat_id=None):
        self.db = db # Instanca Database klase
        self.id = customer_id
        self.name = name
        self.email = email
        self.vat_id = vat_id

    def save(self):
        """ Sprema ili ažurira kupca u bazi podataka. """
        if self.id: # Ažuriranje postojećeg
            query = "UPDATE customers SET name = ?, email = ?, vat_id = ? WHERE id = ?"
            params = (self.name, self.email, self.vat_id, self.id)
            self.db.execute_query(query, params)
        else: # Dodavanje novog
            query = "INSERT INTO customers (name, email, vat_id) VALUES (?, ?, ?)"
            params = (self.name, self.email, self.vat_id)
            cursor = self.db.execute_query(query, params)
            if cursor:
                self.id = cursor.lastrowid # Dohvati ID novokreiranog kupca
        print(f"Kupac '{self.name}' spremljen/ažuriran.")

    @staticmethod
    def get_by_id(db, customer_id):
        """ Dohvaća kupca po ID-u. """
        query = "SELECT * FROM customers WHERE id = ?"
        row = db.fetch_one_query(query, (customer_id,))
        if row:
            return Customer(db, row['id'], row['name'], row['email'], row['vat_id'])
        return None

    @staticmethod
    def get_all(db):
        """ Dohvaća sve kupce. """
        query = "SELECT * FROM customers"
        rows = db.fetch_query(query)
        customers = []
        for row in rows:
            customers.append(Customer(db, row['id'], row['name'], row['email'], row['vat_id']))
        return customers

    def delete(self):
        """ Briše kupca iz baze podataka. """
        if self.id:
            query = "DELETE FROM customers WHERE id = ?"
            self.db.execute_query(query, (self.id,))
            print(f"Kupac s ID {self.id} obrisan.")
            self.id = None # Resetiraj ID objekta
        else:
            print("Ne mogu obrisati kupca bez ID-a.")

    def __str__(self):
        return f"ID: {self.id}, Ime: {self.name}, Email: {self.email}, VAT_id: {self.vat_id}"