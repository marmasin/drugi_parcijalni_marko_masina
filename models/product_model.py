class Product:
    def __init__(self, db, product_id=None, name=None, price=None, description=None):
        self.db = db
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description

    def save(self):
        if self.id:
            query = "UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?"
            params = (self.name, self.price, self.description, self.id)
            self.db.execute_query(query, params)
        else:
            query = "INSERT INTO products (name, price, description) VALUES (?, ?, ?)"
            params = (self.name, self.price, self.description)
            cursor = self.db.execute_query(query, params)
            if cursor:
                self.id = cursor.lastrowid
        print(f"Proizvod '{self.name}' spremljen/ažuriran.")

    def get_by_id(db, product_id):
        query = "SELECT * FROM products WHERE id = ?"
        row = db.fetch_one_query(query, (product_id,))
        if row:
            return Product(db, row['id'], row['name'], row['price'], row['description'])
        return None

    def get_all(db):
        query = "SELECT * FROM products"
        rows = db.fetch_query(query)
        products = []
        for row in rows:
            products.append(Product(db, row['id'], row['name'], row['price'], row['description']))
        return products

    def delete(self):
        if self.id:
            query = "DELETE FROM products WHERE id = ?"
            self.db.execute_query(query, (self.id,))
            print(f"Proizvod s ID {self.id} obrisan.")
            self.id = None
        else:
            print("Ne mogu obrisati proizvod bez ID-a.")


    def __str__(self):
        return f"ID: {self.id}, Naziv: {self.name}, Cijena: {self.price:.2f} EUR, Opis: {self.description}"