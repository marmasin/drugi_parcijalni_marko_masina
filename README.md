# Parcijalni ispit - Napredni koncepti programiranja u programskom jeziku Python

## Zadaci

1. Refaktorirati postojeće rješenje iz Modula 2 kako bi koristili modularnu arhitekturu.
2. Uvesti SQLite bazu podataka za trajno pohranjivanje podataka umjesto JSON datoteka.
3. Kreirati REST API klijent za dohvaćanje podataka o korisnicima i prikazivanje prijavljenog korisnika.
4. Razdvojiti korisničko sučelje u zaseban modul i proširiti ga prikazom korisnika i tvrtke u zaglavlju.


## Upute za Rješavanje Zadatka

1. **Priprema okruženja:**
   - Kreirajte "fork" repozitorija.
   - Dodijelite repozitoriju naziv u formatu `drugi_parcijalni_ime_prezime` (primjer: `drugi_parcijalni_pero_peric`). 
   - **VAŽNO:** Nemojte kreirati "clone" repozitorija jer nemate pravo mijenjanja.

2. **Postavljanje Projekta:**
   - Nakon što ste kreirali fork, klonirajte repozitorij s vašeg GitHub profila na lokalno računalo koristeći GitHub Desktop ili drugu omiljenu metodu.
   - **Nakon kloniranja**, kreirajte novu lokalnu granu nazvanu `ispit`
   - Sve promjene unosite isključivo unutar grane ispit
   - Instalirajte sve potrebne module pomoću `requirements.txt` kako biste osigurali da aplikacija ima sve potrebne biblioteke.

3. **Refaktoriranje postojećeg koda:**
   - Kreirajte direktorij `models/` i unutar njega kreirajte module:
     - `customer_model.py` za rad s kupcima.
     - `product_model.py` za rad s proizvodima.
     - `offer_model.py` za rad s ponudama.
   - Svaki modul treba sadržavati klasu koja predstavlja odgovarajuće entitete (npr. `Customer`, `Product`, `Offer`), uključujući metode za interakciju s bazom podataka.

4. **Kreiranje SQLite baze podataka:**
   - Dodajte datoteku `database.py` koja sadrži klasu za upravljanje bazom (koristeći `sqlite3`).
   - Kreirajte tablice za `customers`, `products`, i `offers`.
   - Implementirajte metode za:
     - Dodavanje novih zapisa.
     - Ažuriranje postojećih zapisa.
     - Dohvaćanje zapisa na temelju upita.

5. **REST API integracija:**
   - Kreirajte direktorij `services/` i unutar njega modul `user_service.py`.
   - Koristite biblioteku `requests` za dohvaćanje podataka s endpointa `https://jsonplaceholder.typicode.com/users`.
   - Implementirajte metodu koja dohvaća podatke o korisnicima i omogućuje korisniku odabir jednog korisnika kao trenutno prijavljenog.

6. **Korisničko sučelje:**
   - Kreirajte modul `user_interface.py` koji:
     - Generira tekstualni izbornik i prikazuje opcije.
     - Prikazuje podatke o prijavljenom korisniku i tvrtki u zaglavlju.
   - Proširite sučelje tako da, uz trenutne funkcionalnosti, uvijek prikazuje:
     - Ime i email prijavljenog korisnika.
     - Informacije o tvrtki (npr. naziv, email, VAT ID).

7. **Implementacija logike za prijavljenog korisnika:**
   - U glavnom modulu (`main.py`) inicijalizirajte prijavljenog korisnika koristeći REST API integraciju.
   - Prikazujte podatke o prijavljenom korisniku u svim dijelovima aplikacije.


#### Očekivani rezultat:
- Aplikacija koristi SQLite za trajno pohranjivanje podataka.
- Kod je organiziran u module (`models`, `services`, `user_interface`).
- Korisničko sučelje je unaprijeđeno i modularizirano.
- API integracija omogućuje dinamičko prikazivanje podataka o korisnicima.

#### Primjer strukture direktorija:
```
offers_calculator/
│
├── main.py
├── database.py
├── user_interface.py
├── services/
│   └── user_service.py
├── models/
│   ├── customer_model.py
│   ├── product_model.py
│   └── offer_model.py
└── db.sqlite3
```

#### Napomena:
- Prilikom implementacije vodite računa o modularnosti i slojevima aplikacije. Koristite klase za sve glavne funkcionalnosti i pridržavajte se zadane strukture aplikacije.

### Dodatne Upute

-  **Rješenja koja imaju mijenjan ostatak koda neće biti ocijenjena.**
- Uporabite `TypeHints` prema uputama u komentarima kako biste osigurali konzistentnost tipova podataka.

## Podnošenje Rješenja

1. Nakon što završite implementaciju:
   - Napravite commit za sve promjene koje ste unijeli koristeći opciju `git commit`.
   - Pushajte granu na vaš GitHub repozitorij `git push`.
  
     
2. Otvorite **Pull Request** iz grane `ispit` prema grani `main`.

   - U Pull Requestu:
     - **Autor:** Vaše ime – osoba koja je radila ispit
     - **Reviewer:** Predavač (kojem ste dali pristup kao suradniku)

       
2. **Podjela Repozitorija s Predavačem**:
   - Otvorite vaš repozitorij na GitHubu.
   - Kliknite na karticu **Settings** (Postavke) u repozitoriju.
   - Pronađite opciju **Collaborators** (Suradnici) i dodajte predavača kao **Contributor**.
   - Unesite GitHub korisničko ime predavača, odaberite ga s popisa, te mu pošaljite pozivnicu za pristup.
   - Predavač će imati pravo pregledati vaš kod i provjeriti zadatke.

> ⚠️ Provjerite da su sve promjene **commitane i pushane** prije nego što dodate predavača, kako bi mogao vidjeti kompletno rješenje.

> **Napomena:** Ako se upute ne budu striktno slijedile, ispit neće biti pregledan.

> **Rok predaje:** 28.5.2025 do 21:00h

---

**Sretno!**
