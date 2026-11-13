"""Smart Grocery Store Management System
Uses lists and dictionaries to manage products and sales.
"""

# ---------------- Data storage ----------------
# List of dictionaries: one dictionary per product
products = [
    {"id": 101, "name": "Milk", "category": "Dairy", "price": 250, "stock": 20},
    {"id": 102, "name": "Bread", "category": "Bakery", "price": 120, "stock": 4},
    {"id": 103, "name": "Rice", "category": "Grains", "price": 400, "stock": 50},
]

# Separate list of dictionaries for completed sales
sales = []


# ---------------- Input helpers (validation) ----------------
def get_int(prompt, minimum=0):
    """Keep asking until the user enters a whole number >= minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a number {minimum} or greater.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt, minimum=0):
    """Keep asking until the user enters a valid number > minimum."""
    while True:
        try:
            value = float(input(prompt))
            if value <= minimum:
                print(f"Please enter a value greater than {minimum}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty.")


def find_product_by_id(product_id):
    """Loop through products and return the matching dictionary, or None."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


# ---------------- Features ----------------
def add_product():
    """Add a new product; duplicate IDs are not allowed."""
    print("\n--- Add New Product ---")
    product_id = get_int("Enter Product ID: ", 1)

    if find_product_by_id(product_id) is not None:
        print("Error: A product with this ID already exists.")
        return

    new_product = {
        "id": product_id,
        "name": get_text("Enter Product Name: "),
        "category": get_text("Enter Category: "),
        "price": get_float("Enter Price: "),
        "stock": get_int("Enter Available Stock: "),
    }
    products.append(new_product)  # add dictionary to the list
    print(f"'{new_product['name']}' added successfully.")


def display_products():
    """Show all products in a readable table."""
    print("\n--- All Products ---")
    if not products:
        print("No products available.")
        return

    print(f"{'ID':<8}{'Name':<20}{'Category':<15}{'Price':<10}{'Stock':<8}")
    print("-" * 61)
    for product in products:
        print(f"{product['id']:<8}{product['name']:<20}{product['category']:<15}"
              f"{product['price']:<10}{product['stock']:<8}")


def search_product():
    """Search by ID or name (name search is case-insensitive)."""
    print("\n--- Search Product ---")
    term = get_text("Enter Product ID or Name: ")
    found = False

    for product in products:
        # Match on ID (if term is numeric) or on name
        if (term.isdigit() and product["id"] == int(term)) or \
           product["name"].lower() == term.lower():
            print(f"\nID:       {product['id']}")
            print(f"Name:     {product['name']}")
            print(f"Category: {product['category']}")
            print(f"Price:    {product['price']}")
            print(f"Stock:    {product['stock']}")
            found = True

    if not found:
        print("Product not found.")


def update_stock():
    """Add stock to, or set the exact quantity of, a product."""
    print("\n--- Update Product Stock ---")
    product = find_product_by_id(get_int("Enter Product ID: ", 1))
    if product is None:
        print("Product not found.")
        return

    print(f"Current stock of {product['name']}: {product['stock']}")
    print("1. Add stock")
    print("2. Set new quantity")
    choice = input("Choose option: ").strip()

    if choice == "1":
        product["stock"] += get_int("Quantity to add: ", 1)
    elif choice == "2":
        product["stock"] = get_int("New quantity: ")
    else:
        print("Invalid option.")
        return

    print(f"Updated stock of {product['name']}: {product['stock']}")


def process_sale():
    """Sell a product: validate, deduct stock, record the sale."""
    print("\n--- Process Customer Sale ---")
    product = find_product_by_id(get_int("Enter Product ID: ", 1))
    if product is None:
        print("Product not found.")
        return

    quantity = get_int("Enter purchase quantity: ", 1)

    # Do not allow sale if stock is insufficient
    if quantity > product["stock"]:
        print(f"Sale denied. Only {product['stock']} unit(s) in stock.")
        return

    total = quantity * product["price"]
    product["stock"] -= quantity  # deduct from stock

    # Record the completed sale
    sales.append({
        "id": product["id"],
        "name": product["name"],
        "quantity": quantity,
        "total": total,
    })

    print("\n--- Purchase Summary ---")
    print(f"Product:     {product['name']}")
    print(f"Quantity:    {quantity}")
    print(f"Unit Price:  {product['price']}")
    print(f"Total:       {total}")
    print(f"Stock Left:  {product['stock']}")


def view_sales():
    """Display all recorded sales."""
    print("\n--- Sales Records ---")
    if not sales:
        print("No sales recorded yet.")
        return

    print(f"{'ID':<8}{'Name':<20}{'Qty':<8}{'Total':<10}")
    print("-" * 46)
    for sale in sales:
        print(f"{sale['id']:<8}{sale['name']:<20}{sale['quantity']:<8}{sale['total']:<10}")


def generate_report():
    """Display summary statistics for the store."""
    print("\n====== STORE REPORT ======")
    if not products:
        print("No products in the system.")
        return

    total_stock = 0
    for product in products:
        total_stock += product["stock"]

    total_revenue = 0
    for sale in sales:
        total_revenue += sale["total"]

    print(f"Total products:           {len(products)}")
    print(f"Total available stock:    {total_stock}")
    print(f"Total sales transactions: {len(sales)}")
    print(f"Total revenue:            {total_revenue}")

    # Products with stock below 5
    print("\nLow stock products (below 5 units):")
    low_found = False
    for product in products:
        if product["stock"] < 5:
            print(f"  - {product['name']} ({product['stock']} left)")
            low_found = True
    if not low_found:
        print("  None")

    # Highest and lowest priced products
    highest = products[0]
    lowest = products[0]
    for product in products:
        if product["price"] > highest["price"]:
            highest = product
        if product["price"] < lowest["price"]:
            lowest = product

    print(f"\nHighest priced: {highest['name']} ({highest['price']})")
    print(f"Lowest priced:  {lowest['name']} ({lowest['price']})")


# ---------------- Main menu ----------------
def main():
    """Show the menu repeatedly until the user chooses Exit."""
    while True:
        print("\n====================================")
        print("SMART GROCERY STORE SYSTEM")
        print("====================================")
        print("1. Add New Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product Stock")
        print("5. Process Customer Sale")
        print("6. View Sales Records")
        print("7. Generate Store Report")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            display_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_stock()
        elif choice == "5":
            process_sale()
        elif choice == "6":
            view_sales()
        elif choice == "7":
            generate_report()
        elif choice == "8":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()