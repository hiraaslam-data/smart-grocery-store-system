# 🛒 Smart Grocery Store Management System

**Author:** Hira Aslam  
**Language:** Python 3.x  
**File:** `grocery_store.py`

---

## 📖 Overview

The **Smart Grocery Store Management System** is a lightweight, terminal-based Python application designed to streamline daily grocery store operations. It provides a user-friendly command-line interface (CLI) to manage product inventory, track customer sales, and generate insightful business reports. 

Built entirely with standard Python data structures (Lists and Dictionaries), this system requires no external databases or libraries, making it incredibly fast and easy to deploy.

---

## ⚙️ Code Structure & Function Explanations

The script is modular and divided into specific functions handling validation, data retrieval, and core features. Here is a complete explanation of every function written in the code:

### 1. Data Storage Variables
*   **`products` (List of Dictionaries):** Acts as the main database for the inventory. Each dictionary contains keys for `id`, `name`, `category`, `price`, and `stock`. Pre-loaded with three dummy items (Milk, Bread, Rice).
*   **`sales` (List of Dictionaries):** Acts as the ledger. It starts empty and gets populated whenever a sale is processed.

### 2. Input Helpers (Validation Functions)
These functions are designed to prevent the program from crashing if a user enters incorrect data types (like typing text when a number is asked).
*   **`get_int(prompt, minimum=0)`:** Uses a `while True` loop and a `try-except` block to force the user to enter a valid whole number (integer). It checks if the number is greater than or equal to the `minimum` value provided.
*   **`get_float(prompt, minimum=0)`:** Similar to `get_int`, but accepts decimal values (floats) for currency inputs like price. It ensures the value is strictly greater than the `minimum`.
*   **`get_text(prompt)`:** Ensures the user does not submit an empty string or just spaces. It uses the `.strip()` method and loops until valid text is entered.

### 3. Utility Functions
*   **`find_product_by_id(product_id)`:** A helper function that loops through the `products` list. If it finds a dictionary where the `id` matches the input, it returns that specific dictionary. If no match is found, it returns `None`.

### 4. Core Feature Functions
*   **`add_product()`:** 
    *   Prompts the user for a new Product ID.
    *   Calls `find_product_by_id()` to check if the ID already exists. If it does, it rejects the entry to prevent duplicates.
    *   Collects name, category, price, and stock using the validation helpers.
    *   Creates a `new_product` dictionary and appends it to the `products` list.
*   **`display_products()`:** 
    *   Checks if the `products` list is empty.
    *   If not, it prints a dynamically formatted table header and loops through all items in the inventory, formatting their attributes neatly into columns using f-string spacing (`:<8`, `:<20`, etc.).
*   **`search_product()`:** 
    *   Asks the user for a search term (can be text or numbers).
    *   Loops through the inventory. It checks if the term matches an integer ID (using `.isdigit()`) **OR** if it matches a product name.
    *   Uses `.lower()` to ensure name searches are case-insensitive (e.g., "milk" matches "Milk").
*   **`update_stock()`:** 
    *   Finds a product via its ID.
    *   Offers a sub-menu with two choices: `1. Add stock` (adds to the existing value) or `2. Set new quantity` (overwrites the existing value completely).
    *   Updates the specific dictionary's `stock` key based on the choice.
*   **`process_sale()`:** 
    *   Validates the product ID and asks for a purchase quantity.
    *   **Crucial check:** If the requested quantity is greater than the available `product["stock"]`, the sale is denied.
    *   Calculates the `total` (quantity * price).
    *   Deducts the quantity from the inventory `stock`.
    *   Appends a new dictionary containing the sale details to the `sales` list.
*   **`view_sales()`:** 
    *   Checks if the `sales` list has any records.
    *   Loops through the `sales` list and prints a formatted table showing ID, Name, Quantity Sold, and Total Revenue per transaction.
*   **`generate_report()`:** 
    *   Calculates aggregate data: uses loops to sum up `total_stock` across all products and `total_revenue` across all sales.
    *   Prints total products and total transactions using `len()`.
    *   **Low Stock Alert:** Loops through products and flags any item with a `stock` below 5.
    *   **Price Analytics:** Initializes the first product as both the `highest` and `lowest` priced item, then iterates through the list to compare and find the actual highest and lowest priced items in the system.
*   **`main()`:** 
    *   The entry point of the program.
    *   Contains a `while True` loop that continuously displays the 8-option main menu.
    *   Reads the user's choice and calls the corresponding feature function.
    *   Breaks the loop and exits the program gracefully when option 8 is selected.

---

## 🚀 Installation & Usage

### Prerequisites
You only need **Python 3.x** installed on your computer. No external packages are required.

### How to Run the Program
1. Download the source code to your local machine as `grocery_store.py`.
2. Open your Terminal (Mac/Linux) or Command Prompt / PowerShell (Windows).
3. Navigate to the folder containing the file:
   ```bash
   cd path/to/your/folder
   ```
4. Run the script:
   ```bash
   python grocery_store.py
   ```

## 🛡️ Error Handling Details
The system is heavily fortified against user errors:
*   **Empty Inputs:** Handled by `get_text()`.
*   **Invalid Types (e.g., Letters for ID/Price):** Trapped by `ValueError` exceptions in `get_int()` and `get_float()`.
*   **Logical Constraints:** Stock limits are enforced during sales, and duplicate IDs are blocked during product creation.

---
*Created and maintained by **Hira Aslam**.*