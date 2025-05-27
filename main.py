import json
from datetime import datetime

OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def create_new_offer(offers, products, customers):
    offer_number = len(offers) + 1
    print("Select a customer for the offer:")
    for idx, customer in enumerate(customers, 1):
        print(f"{idx}. {customer['name']} ({customer['email']})")

    customer_choice = int(input("Select a customer by number: ")) - 1
    customer = customers[customer_choice]
    date = input("Enter offer date (YYYY-MM-DD): ")
    tax_rate = float(input("Enter tax rate (%): ")) / 100
    items = []

    while True:
        print("Available products:")
        for product in products:
            print(f"{product['id']}. {product['name']} - ${product['price']} - {product['description']}")
        product_id = int(input("Enter product ID to add (0 to finish): "))

        if product_id == 0:
            break

        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            quantity = int(input("Enter quantity: "))
            item_total = product["price"] * quantity
            items.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "quantity": quantity,
                "item_total": item_total
            })
        else:
            print("Product not found. Please try again.")

    sub_total = sum(item["item_total"] for item in items)
    tax = sub_total * tax_rate
    total = sub_total + tax

    offer = {
        "offer_number": offer_number,
        "customer": customer,
        "date": date,
        "items": items,
        "sub_total": sub_total,
        "tax": tax,
        "total": total
    }
    offers.append(offer)
    save_data(OFFERS_FILE, offers)
    print("Offer created successfully.")


def manage_products(products):
    action = input("Do you want to add a new product or modify an existing one? (add/modify): ").lower()

    if action == "add":
        product_id = len(products) + 1
        product_name = input("Enter product name: ")
        product_description = input("Enter product description: ")
        product_price = float(input("Enter product price: "))
        product = {"id": product_id, "name": product_name, "description": product_description, "price": product_price}
        products.append(product)
        save_data(PRODUCTS_FILE, products)
        print("Product added successfully.")

    elif action == "modify":
        print("Available products:")
        for product in products:
            print(f"{product['id']}. {product['name']} - ${product['price']} - {product['description']}")
        product_id = int(input("Enter product ID to modify: "))
        product = next((p for p in products if p["id"] == product_id), None)

        if product:
            new_name = input("Enter new name (leave blank to keep current): ")
            new_description = input("Enter new description (leave blank to keep current): ")
            new_price = input("Enter new price (leave blank to keep current): ")
            if new_name:
                product["name"] = new_name
            if new_description:
                product["description"] = new_description
            if new_price:
                product["price"] = float(new_price)
            save_data(PRODUCTS_FILE, products)
            print("Product modified successfully.")
        else:
            print("Product not found.")


def manage_customers(customers):
    action = input("Do you want to add a new customer or view all customers? (add/view): ").lower()

    if action == "add":
        customer_name = input("Enter customer name: ")
        customer_email = f"info@{customer_name.replace(' ', '').lower()}.com"
        customer_vat_id = input("Enter customer VAT ID (11-digit number): ")
        customer = {
            "name": customer_name,
            "email": customer_email,
            "vat_id": customer_vat_id
        }
        customers.append(customer)
        save_data(CUSTOMERS_FILE, customers)
        print("Customer added successfully.")

    elif action == "view":
        print("Customer List:")
        for customer in customers:
            print(f"Name: {customer['name']}, Email: {customer['email']}, VAT ID: {customer['vat_id']}")
    else:
        print("Invalid choice.")


def display_offers(offers):
    choice = input("View all offers, offers by month, or a single offer? (all/month/single): ").lower()

    if choice == "all":
        for offer in offers:
            print_offer(offer)

    elif choice == "month":
        month = input("Enter month (MM): ")
        for offer in offers:
            offer_date = datetime.strptime(offer["date"], "%Y-%m-%d")
            if offer_date.strftime("%m") == month:
                print_offer(offer)

    elif choice == "single":
        offer_number = int(input("Enter offer number: "))
        for offer in offers:
            if offer["offer_number"] == offer_number:
                print_offer(offer)
                break
        else:
            print("Offer not found.")


def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']['name']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()
