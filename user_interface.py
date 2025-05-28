from models.customer_model import Customer
from models.product_model import Product
from models.offer_model import Offer

class UserInterface:
    def __init__(self, db_instance, user_service_instance):
        self.db = db_instance
        self.user_service = user_service_instance

    def display_header(self):
        """ Prikazuje zaglavlje s informacijama o prijavljenom korisniku i tvrtki. """
        user_info = self.user_service.get_current_user_info()
        if user_info:
            print("-" * 50)
            print("APLIKACIJA ZA KREIRANJE PONUDA")
            print("-" * 50)
            print(f"Prijavljeni korisnik: {user_info['name']} ({user_info['email']})")
            print(f"Tvrtka: {user_info['company_name']} (VAT ID: {user_info['vat_id']})")
            print(f"Moto tvrtke: \"{user_info['company_catchphrase']}\"")
            print("-" * 50)
        else:
            print("-" * 50)
            print("APLIKACIJA ZA KREIRANJE PONUDA")
            print("Nijedan korisnik nije prijavljen.")
            print("-" * 50)

    def display_main_menu(self):
        """ Prikazuje glavni izbornik. """
        print("\nGlavni izbornik:")
        print("1. Upravljanje kupcima")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje ponudama")
        print("4. Promijeni prijavljenog korisnika")
        print("0. Izlaz")
        return input("Odaberite opciju: ")

    def manage_customers_menu(self):
        while True:
            self.display_header()
            print("\n--- Upravljanje kupcima ---")
            print("1. Dodaj novog kupca")
            print("2. Prikaži sve kupce")
            print("3. Ažuriraj kupca")
            print("4. Obriši kupca")
            print("0. Povratak na glavni izbornik")
            choice = input("Odabir: ")

            if choice == '1':
                name = input("Unesite ime kupca: ")
                email = input("Unesite email kupca: ")
                vat_id = input("Unesite vat_id kupca: ")
                customer = Customer(self.db, name=name, email=email, vat_id=vat_id)
                customer.save()
            elif choice == '2':
                customers = Customer.get_all(self.db)
                if customers:
                    print("\n--- Popis svih kupaca ---")
                    for cust in customers:
                        print(cust)
                else:
                    print("Nema unesenih kupaca.")
            elif choice == '3':
                customer_id = int(input("Unesite ID kupca za ažuriranje: "))
                customer = Customer.get_by_id(self.db, customer_id)
                if customer:
                    print(f"Trenutni podaci: {customer}")
                    customer.name = input(f"Novo ime ({customer.name}): ") or customer.name
                    customer.email = input(f"Novi email ({customer.email}): ") or customer.email
                    customer.vat_id = input(f"Novi vat_id ({customer.vat_id}): ") or customer.vat_id
                    customer.save()
                else:
                    print(f"Kupac s ID {customer_id} nije pronađen.")
            elif choice == '4':
                customer_id = int(input("Unesite ID kupca za brisanje: "))
                customer = Customer.get_by_id(self.db, customer_id)
                if customer:
                    confirm = input(f"Jeste li sigurni da želite obrisati kupca '{customer.name}'? (da/ne): ")
                    if confirm.lower() == 'da':
                        customer.delete()
                else:
                    print(f"Kupac s ID {customer_id} nije pronađen.")
            elif choice == '0':
                break
            else:
                print("Neispravan unos.")
            input("\nPritisnite Enter za nastavak...")


    def manage_products_menu(self):
        while True:
            self.display_header()
            print("\n--- Upravljanje proizvodima ---")
            print("1. Dodaj novi proizvod")
            print("2. Prikaži sve proizvode")
            print("3. Ažuriraj proizvod")
            print("4. Obriši proizvod")
            print("0. Povratak na glavni izbornik")
            choice = input("Odabir: ")

            if choice == '1':
                name = input("Unesite naziv proizvoda: ")
                try:
                    price = float(input("Unesite cijenu proizvoda: "))
                except ValueError:
                    print("Neispravan unos za cijenu.")
                    continue
                description = input("Unesite opis proizvoda: ")
                product = Product(self.db, name=name, price=price, description=description)
                product.save()
            elif choice == '2':
                products = Product.get_all(self.db)
                if products:
                    print("\n--- Popis svih proizvoda ---")
                    for prod in products:
                        print(prod)
                else:
                    print("Nema unesenih proizvoda.")
            elif choice == '3':
                try:
                    product_id = int(input("Unesite ID proizvoda za ažuriranje: "))
                except ValueError:
                    print("Neispravan ID.")
                    continue
                product = Product.get_by_id(self.db, product_id)
                if product:
                    print(f"Trenutni podaci: {product}")
                    product.name = input(f"Novi naziv ({product.name}): ") or product.name
                    try:
                        new_price_str = input(f"Nova cijena ({product.price}): ")
                        if new_price_str: # Provjeri je li string prazan prije konverzije
                             product.price = float(new_price_str)
                    except ValueError:
                        print("Neispravan unos za cijenu, cijena nije promijenjena.")
                    product.description = input(f"Novi opis ({product.description}): ") or product.description
                    product.save()
                else:
                    print(f"Proizvod s ID {product_id} nije pronađen.")
            elif choice == '4':
                try:
                    product_id = int(input("Unesite ID proizvoda za brisanje: "))
                except ValueError:
                    print("Neispravan ID.")
                    continue
                product = Product.get_by_id(self.db, product_id)
                if product:
                    confirm = input(f"Jeste li sigurni da želite obrisati proizvod '{product.name}'? (da/ne): ")
                    if confirm.lower() == 'da':
                        product.delete()
                else:
                    print(f"Proizvod s ID {product_id} nije pronađen.")
            elif choice == '0':
                break
            else:
                print("Neispravan unos.")
            input("\nPritisnite Enter za nastavak...")

    def manage_offers_menu(self):
        while True:
            self.display_header()
            print("\n--- Upravljanje ponudama ---")
            print("1. Kreiraj novu ponudu")
            print("2. Prikaži sve ponude")
            print("3. Prikaži detalje ponude")
            print("4. Obriši ponudu") # Dodana opcija za brisanje
            print("0. Povratak na glavni izbornik")
            choice = input("Odabir: ")

            if choice == '1':
                self.create_new_offer()
            elif choice == '2':
                self.display_all_offers()
            elif choice == '3':
                self.display_offer_details()
            elif choice == '4':
                self.delete_offer()
            elif choice == '0':
                break
            else:
                print("Neispravan unos.")
            input("\nPritisnite Enter za nastavak...")

    def create_new_offer(self):
        self.display_header()
        print("\n--- Kreiranje nove ponude ---")
        customers = Customer.get_all(self.db)
        if not customers:
            print("Nema kupaca u bazi. Prvo dodajte kupca.")
            return

        print("Dostupni kupci:")
        for i, cust in enumerate(customers):
            print(f"{i + 1}. {cust.name} (ID: {cust.id})")
        
        try:
            cust_choice_idx = int(input("Odaberite broj kupca: ")) - 1
            if not (0 <= cust_choice_idx < len(customers)):
                print("Neispravan odabir kupca.")
                return
            selected_customer_id = customers[cust_choice_idx].id
        except ValueError:
            print("Neispravan unos za kupca.")
            return

        new_offer = Offer(self.db, customer_id=selected_customer_id)
        
        products = Product.get_all(self.db)
        if not products:
            print("Nema proizvoda u bazi. Dodajte proizvode prije kreiranja ponude.")
            return

        while True:
            print("\nDostupni proizvodi:")
            for i, prod in enumerate(products):
                print(f"{i + 1}. {prod.name} - {prod.price:.2f} EUR (ID: {prod.id})")
            print("0. Završi dodavanje stavki i spremi ponudu")

            try:
                prod_choice_idx = int(input("Odaberite broj proizvoda za dodavanje (ili 0 za kraj): ")) - 1
                if prod_choice_idx == -1: # Korisnik odabrao 0
                    break 
                if not (0 <= prod_choice_idx < len(products)):
                    print("Neispravan odabir proizvoda.")
                    continue
                
                selected_product = products[prod_choice_idx]
                quantity = int(input(f"Unesite količinu za '{selected_product.name}': "))
                if quantity <= 0:
                    print("Količina mora biti veća od 0.")
                    continue
                
                new_offer.add_item(selected_product, quantity)
                print(f"Proizvod '{selected_product.name}' dodan u ponudu.")

            except ValueError:
                print("Neispravan unos.")
        
        if new_offer.items: # Spremi ponudu samo ako ima stavki
            new_offer.save()
            print(f"Nova ponuda (ID: {new_offer.id}) je uspješno kreirana i spremljena.")
            print(new_offer) # Ispiši detalje kreirane ponude
        else:
            print("Ponuda nije spremljena jer nema stavki.")


    def display_all_offers(self):
        self.display_header()
        print("\n--- Popis svih ponuda ---")
        offers = Offer.get_all(self.db)
        if offers:
            for offer_summary in offers:
                customer_name = "Nepoznat"
                if offer_summary.customer_id:
                    customer = Customer.get_by_id(self.db, offer_summary.customer_id)
                    if customer:
                        customer_name = customer.name
                print(f"ID: {offer_summary.id}, Kupac: {customer_name}, Datum: {offer_summary.offer_date}, Ukupno: {offer_summary.total_amount:.2f} EUR")
        else:
            print("Nema kreiranih ponuda.")

    def display_offer_details(self):
        self.display_header()
        try:
            offer_id = int(input("Unesite ID ponude za prikaz detalja: "))
        except ValueError:
            print("Neispravan ID.")
            return
        
        offer = Offer.get_by_id(self.db, offer_id)
        if offer:
            print("\n--- Detalji ponude ---")
            print(offer) # __str__ metoda Offer klase će formatirati ispis
        else:
            print(f"Ponuda s ID {offer_id} nije pronađena.")

    def delete_offer(self):
        self.display_header()
        try:
            offer_id = int(input("Unesite ID ponude za brisanje: "))
        except ValueError:
            print("Neispravan ID.")
            return
        
        offer = Offer.get_by_id(self.db, offer_id) # Dohvati ponudu da potvrdimo da postoji
        if offer:
            confirm = input(f"Jeste li sigurni da želite obrisati ponudu ID {offer.id}? (da/ne): ")
            if confirm.lower() == 'da':
                offer.delete() # Pozovi metodu delete na instanci
            else:
                print("Brisanje otkazano.")
        else:
            print(f"Ponuda s ID {offer_id} nije pronađena.")