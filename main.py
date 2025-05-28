from database import Database
from services.user_service import UserService
from user_interface import UserInterface

def main():
    # 1. Inicijalizacija baze podataka
    db = Database(db_name="Baza.db")
    db.connect()
    db.create_tables()

    # 2. Inicijalizacija servisa za korisnike
    user_service = UserService()
    
    # 3. Dohvaćanje i odabir prijavljenog korisnika
    print("--- Prijava Korisnika ---")
    if not user_service.fetch_users():
        print("Nije moguće dohvatiti korisnike s API-ja. Aplikacija se ne može nastaviti bez korisnika.")
        db.disconnect()
        return
        
    selected_user = user_service.select_user()
    if not selected_user:
        print("Nijedan korisnik nije odabran. Izlaz iz aplikacije.")
        db.disconnect()
        return

    # 4. Inicijalizacija korisničkog sučelja
    ui = UserInterface(db, user_service)

    # 5. Glavna petlja aplikacije
    while True:
        ui.display_header() # Prikazuje se na početku svakog ciklusa petlje
        choice = ui.display_main_menu()

        if choice == '1':
            ui.manage_customers_menu()
        elif choice == '2':
            ui.manage_products_menu()
        elif choice == '3':
            ui.manage_offers_menu()
        elif choice == '4':
            print("\n--- Promjena prijavljenog korisnika ---")
            user_service.select_user() # Omogući ponovni odabir
            # Nema potrebe za ponovnom inicijalizacijom ui objekta jer on već ima referencu na user_service
        elif choice == '0':
            print("Izlaz iz aplikacije...")
            break
        else:
            print("Neispravan odabir, pokušajte ponovno.")
            input("\nPritisnite Enter za nastavak...")


    # 6. Zatvaranje veze s bazom podataka pri izlasku
    db.disconnect()

if __name__ == "__main__":
    main()