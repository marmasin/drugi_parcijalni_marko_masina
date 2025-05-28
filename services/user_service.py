import requests

API_URL = "https://jsonplaceholder.typicode.com/users"

class UserService:
    def __init__(self):
        self.users = []
        self.selected_user = None

    def fetch_users(self):
        """ Dohvaća korisnike s vanjskog API-ja. """
        try:
            response = requests.get(API_URL)
            response.raise_for_status()  # Provjerava HTTP greške (4xx ili 5xx)
            self.users = response.json()
            print(f"Dohvaćeno {len(self.users)} korisnika s API-ja.")
            return self.users
        except requests.exceptions.RequestException as e:
            print(f"Greška pri dohvaćanju korisnika: {e}")
            self.users = []
            return []

    def select_user(self):
        """ Omogućava korisniku odabir prijavljenog korisnika. """
        if not self.users:
            print("Nema dostupnih korisnika za odabir. Prvo dohvatite korisnike.")
            if not self.fetch_users(): # Pokušaj ponovno dohvatiti ako je lista prazna
                 print("Nije moguće dohvatiti korisnike.")
                 return None


        print("\nOdaberite prijavljenog korisnika unosom broja:")
        for i, user in enumerate(self.users):
            print(f"{i + 1}. {user.get('name')} ({user.get('email')})")
        
        while True:
            try:
                choice = int(input("Unesite broj korisnika: ")) - 1
                if 0 <= choice < len(self.users):
                    self.selected_user = self.users[choice]
                    print(f"Odabran korisnik: {self.selected_user.get('name')}")
                    return self.selected_user
                else:
                    print("Neispravan odabir. Pokušajte ponovno.")
            except ValueError:
                print("Neispravan unos. Molimo unesite broj.")
    
    def get_current_user_info(self):
        if self.selected_user:
            user_info = {
                "name": self.selected_user.get('name', 'N/A'),
                "email": self.selected_user.get('email', 'N/A'),
                "company_name": self.selected_user.get('company', {}).get('name', 'N/A'),
                "company_catchphrase": self.selected_user.get('company', {}).get('catchPhrase', 'N/A'),
                "vat_id": "HR12345678901" # JSONPlaceholder nema VAT ID, pa je ovo placeholder
            }
            return user_info
        return None

# Primjer korištenja
if __name__ == '__main__':
    user_service = UserService()
    users_data = user_service.fetch_users()
    if users_data:
        selected = user_service.select_user()
        if selected:
            print("\nDetalji odabranog korisnika:")
            print(f"Ime: {selected.get('name')}")
            print(f"Email: {selected.get('email')}")
            print(f"Tvrtka: {selected.get('company', {}).get('name')}")
            
            current_info = user_service.get_current_user_info()
            print("\nFormatirani info za zaglavlje:")
            print(current_info)