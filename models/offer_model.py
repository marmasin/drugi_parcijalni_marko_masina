from datetime import datetime

class OfferItem:
    def __init__(self, product_id, quantity, unit_price):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price # Cijena u trenutku dodavanja u ponudu

class Offer:
    def __init__(self, db, offer_id=None, customer_id=None, offer_date=None, total_amount=0.0):
        self.db = db
        self.id = offer_id
        self.customer_id = customer_id
        self.offer_date = offer_date if offer_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_amount = total_amount
        self.items = [] # Lista OfferItem objekata

    def add_item(self, product, quantity):
        """ Dodaje proizvod (kao OfferItem) u ponudu. """
        if product and product.id and product.price is not None:
            item = OfferItem(product_id=product.id, quantity=quantity, unit_price=product.price)
            self.items.append(item)
            self.calculate_total()
            print(f"Stavka dodana: Proizvod ID {product.id}, Količina {quantity}")
        else:
            print("Greška: Nije moguće dodati neispravan proizvod u ponudu.")


    def calculate_total(self):
        """ Izračunava ukupan iznos ponude na temelju stavki. """
        self.total_amount = sum(item.quantity * item.unit_price for item in self.items)
        return self.total_amount

    def save(self):
        """ Sprema ponudu i njezine stavke u bazu podataka. """
        self.calculate_total() # Osiguraj da je total_amount ažuriran
        if self.id: # Ažuriranje postojeće ponude (kompleksnije, može uključivati brisanje/dodavanje stavki)
            query = "UPDATE offers SET customer_id = ?, offer_date = ?, total_amount = ? WHERE id = ?"
            params = (self.customer_id, self.offer_date, self.total_amount, self.id)
            self.db.execute_query(query, params)
            
            # Ažuriranje stavki: jednostavna implementacija - briši stare, dodaj nove
            self.db.execute_query("DELETE FROM offer_items WHERE offer_id = ?", (self.id,))
            for item in self.items:
                item_query = "INSERT INTO offer_items (offer_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)"
                item_params = (self.id, item.product_id, item.quantity, item.unit_price)
                self.db.execute_query(item_query, item_params)
        else: # Dodavanje nove ponude
            query = "INSERT INTO offers (customer_id, offer_date, total_amount) VALUES (?, ?, ?)"
            params = (self.customer_id, self.offer_date, self.total_amount)
            cursor = self.db.execute_query(query, params)
            if cursor:
                self.id = cursor.lastrowid
                # Spremi stavke ponude
                for item in self.items:
                    item_query = "INSERT INTO offer_items (offer_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)"
                    item_params = (self.id, item.product_id, item.quantity, item.unit_price)
                    self.db.execute_query(item_query, item_params)
        print(f"Ponuda ID {self.id} spremljena/ažurirana s ukupnim iznosom {self.total_amount:.2f} EUR.")


    @staticmethod
    def get_by_id(db, offer_id):
        """ Dohvaća ponudu po ID-u, uključujući njezine stavke. """
        query = "SELECT * FROM offers WHERE id = ?"
        row = db.fetch_one_query(query, (offer_id,))
        if row:
            offer = Offer(db, row['id'], row['customer_id'], row['offer_date'], row['total_amount'])
            
            # Dohvati stavke ponude
            items_query = """
                SELECT oi.product_id, oi.quantity, oi.unit_price, p.name as product_name
                FROM offer_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.offer_id = ?
            """
            item_rows = db.fetch_query(items_query, (offer.id,))
            offer.items = [] # Resetiraj ako je bilo što od prije
            for item_row in item_rows:
                # Kreiramo 'pseudo' OfferItem samo za prikaz, jer OfferItem nema product_name
                # Možemo dodati product_name u OfferItem ili ga ovako privremeno držati
                loaded_item = OfferItem(item_row['product_id'], item_row['quantity'], item_row['unit_price'])
                setattr(loaded_item, 'product_name', item_row['product_name']) # Dinamički dodajemo ime proizvoda
                offer.items.append(loaded_item)
            return offer
        return None

    @staticmethod
    def get_all(db):
        """ Dohvaća sve ponude (bez detalja o stavkama za sažeti prikaz). """
        query = "SELECT * FROM offers"
        rows = db.fetch_query(query)
        offers = []
        for row in rows:
            # Za get_all, možda ne želimo odmah učitavati sve stavke svake ponude
            # radi performansi. Možemo ih učitati kasnije po potrebi.
            offers.append(Offer(db, row['id'], row['customer_id'], row['offer_date'], row['total_amount']))
        return offers

    def delete(self):
        """ Briše ponudu i njezine stavke iz baze podataka. """
        if self.id:
            # Prvo obriši povezane stavke
            self.db.execute_query("DELETE FROM offer_items WHERE offer_id = ?", (self.id,))
            # Zatim obriši samu ponudu
            self.db.execute_query("DELETE FROM offers WHERE id = ?", (self.id,))
            print(f"Ponuda s ID {self.id} i njezine stavke obrisane.")
            self.id = None
        else:
            print("Ne mogu obrisati ponudu bez ID-a.")

    def __str__(self):
        customer_name = "Nepoznat kupac"
        if self.customer_id:
            from .customer_model import Customer # Lokalni import da se izbjegne circular dependency
            customer = Customer.get_by_id(self.db, self.customer_id)
            if customer:
                customer_name = customer.name
        
        details = f"Ponuda ID: {self.id}\nKupac: {customer_name} (ID: {self.customer_id})\nDatum: {self.offer_date}\nUkupno: {self.total_amount:.2f} EUR\nStavke:\n"
        if self.items:
            for i, item in enumerate(self.items, 1):
                product_name = getattr(item, 'product_name', f"Proizvod ID: {item.product_id}") # Koristi product_name ako postoji
                details += f"  {i}. {product_name} - Količina: {item.quantity}, Cijena po kom: {item.unit_price:.2f} EUR\n"
        else:
            details += "  (Nema stavki)\n"
        return details