"""Smart Grocery Store Management System - menu-driven Python application."""

INITIAL_PRODUCTS = [
    {"id": 101, "name": "Milk", "category": "Dairy", "price": 250.0, "stock": 20},
    {"id": 102, "name": "Bread", "category": "Bakery", "price": 120.0, "stock": 12},
    {"id": 103, "name": "Rice", "category": "Grains", "price": 180.0, "stock": 4},
]
LOW_STOCK_LIMIT = 5
MENU_OPTIONS = {"1", "2", "3", "4", "5", "6", "7", "8"}


def find_product(products, product_id):
    """Return a product matching product_id, or None."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def read_integer(prompt, minimum=1):
    """Read an integer at least minimum; keep asking after invalid input."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
            if value < minimum:
                print(f"Please enter a whole number of at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_price(prompt):
    """Read a positive numeric price."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
            if value <= 0:
                print("Price must be greater than zero.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def add_product(products):
    """Collect and append a new product, rejecting duplicate IDs."""
    product_id = read_integer("Product ID: ")
    if find_product(products, product_id):
        print("Error: that product ID already exists.")
        return False
    name = input("Product name: ").strip()
    while not name:
        print("Product name cannot be empty.")
        name = input("Product name: ").strip()
    category = input("Category: ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip()
    price = read_price("Price: ")
    stock = read_integer("Available stock: ", minimum=0)
    # Keep each product as one dictionary inside the inventory list.
    products.append({"id": product_id, "name": name, "category": category,
                     "price": price, "stock": stock})
    print(f"Product '{name}' added successfully.")
    return True


def display_products(products):
    """Display all products in a readable table."""
    if not products:
        print("No products are currently available.")
        return
    print("\nID   Product              Category         Price       Stock")
    print("-" * 65)
    for product in products:
        print(f"{product['id']:<4} {product['name']:<20} {product['category']:<16} "
              f"Rs. {product['price']:<8.2f} {product['stock']}")


def search_product(products):
    """Search by numeric ID or case-insensitive product name."""
    term = input("Enter product name or ID: ").strip()
    if not term:
        print("Search value cannot be empty.")
        return None
    matches = []
    if term.isdigit():
        product = find_product(products, int(term))
        if product:
            matches.append(product)
    else:
        matches = [p for p in products if term.casefold() in p["name"].casefold()]
    if not matches:
        print("Product not found.")
        return None
    for product in matches:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Category: {product['category']} | Price: Rs. {product['price']:.2f} | "
              f"Stock: {product['stock']}")
    return matches


def update_stock(products):
    """Add stock or replace the current stock quantity."""
    product_id = read_integer("Product ID: ")
    product = find_product(products, product_id)
    if product is None:
        print("Product not found.")
        return False
    print("1. Add stock\n2. Set stock quantity")
    action = input("Choose stock update type: ").strip()
    if action not in {"1", "2"}:
        print("Invalid stock update option.")
        return False
    quantity = read_integer("Quantity: ", minimum=0)
    if action == "1":
        product["stock"] += quantity
    else:
        product["stock"] = quantity
    print(f"Updated stock for {product['name']}: {product['stock']} units.")
    return True


def process_sale(products, sales):
    """Complete a sale only when the product and requested stock are valid."""
    product_id = read_integer("Product ID: ")
    product = find_product(products, product_id)
    if product is None:
        print("Sale rejected: product not found.")
        return False
    quantity = read_integer("Purchase quantity: ")
    # Reject an over-sized order before changing stock or recording a sale.
    if quantity > product["stock"]:
        print(f"Sale rejected: only {product['stock']} unit(s) available.")
        return False
    total = product["price"] * quantity
    # Commit the inventory deduction and matching sales record together.
    product["stock"] -= quantity
    sales.append({"product_id": product["id"], "product_name": product["name"],
                  "quantity_sold": quantity, "total_amount": total})
    print("\nPurchase successful")
    print(f"Product: {product['name']}\nQuantity: {quantity}\nTotal: Rs. {total:.2f}")
    print(f"Remaining stock: {product['stock']}")
    return True


def view_sales(sales):
    """Display completed sales transactions."""
    if not sales:
        print("No sales have been recorded.")
        return
    print("\nProduct ID  Product              Quantity  Total")
    print("-" * 58)
    for sale in sales:
        print(f"{sale['product_id']:<11} {sale['product_name']:<20} "
              f"{sale['quantity_sold']:<9} Rs. {sale['total_amount']:.2f}")


def generate_report(products, sales):
    """Print inventory, revenue, low-stock and price-extreme summary."""
    total_stock = sum(product["stock"] for product in products)
    revenue = sum(sale["total_amount"] for sale in sales)
    print("\n========== STORE REPORT ==========")
    print(f"Total products: {len(products)}")
    print(f"Total available stock: {total_stock}")
    print(f"Total sales transactions: {len(sales)}")
    print(f"Total revenue: Rs. {revenue:.2f}")
    low_stock = [p for p in products if p["stock"] < LOW_STOCK_LIMIT]
    print("Products below 5 units: " + (", ".join(p["name"] for p in low_stock) if low_stock else "None"))
    if products:
        highest = max(products, key=lambda p: p["price"])
        lowest = min(products, key=lambda p: p["price"])
        print(f"Highest-priced product: {highest['name']} (Rs. {highest['price']:.2f})")
        print(f"Lowest-priced product: {lowest['name']} (Rs. {lowest['price']:.2f})")
    else:
        print("Highest-priced product: N/A")
        print("Lowest-priced product: N/A")
    print("==================================")


def show_menu():
    print("\n====================================")
    print("SMART GROCERY STORE SYSTEM")
    print("====================================")
    print("1. Add New Product\n2. View All Products\n3. Search Product\n4. Update Product Stock")
    print("5. Process Customer Sale\n6. View Sales Records\n7. Generate Store Report\n8. Exit")


def main():
    """Run the interactive store menu until the user exits."""
    products = [product.copy() for product in INITIAL_PRODUCTS]
    sales = []
    # Keep the application active until the explicit Exit menu option.
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice not in MENU_OPTIONS:
            print("Invalid menu choice. Please select 1 to 8.")
        elif choice == "1":
            add_product(products)
        elif choice == "2":
            display_products(products)
        elif choice == "3":
            search_product(products)
        elif choice == "4":
            update_stock(products)
        elif choice == "5":
            process_sale(products, sales)
        elif choice == "6":
            view_sales(sales)
        elif choice == "7":
            generate_report(products, sales)
        else:
            print("Thank you for using Smart Grocery Store System. Goodbye!")
            break


if __name__ == "__main__":
    main()
