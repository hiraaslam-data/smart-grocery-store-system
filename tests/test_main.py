"""Automated tests for the Smart Grocery Store Management System."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class GroceryStoreTests(unittest.TestCase):
    def setUp(self):
        self.products = [
            {"id": 1, "name": "Milk", "category": "Dairy", "price": 250.0, "stock": 5},
            {"id": 2, "name": "Bread", "category": "Bakery", "price": 100.0, "stock": 0},
        ]
        self.sales = []

    def capture(self, func, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            result = func(*args)
        return result, output.getvalue()

    def test_add_product_success(self):
        with patch("builtins.input", side_effect=["3", "Eggs", "Dairy", "90", "0"]):
            result, output = self.capture(main.add_product, self.products)
        self.assertTrue(result)
        self.assertEqual(self.products[-1]["stock"], 0)
        self.assertIn("added successfully", output)

    def test_duplicate_id_rejected(self):
        with patch("builtins.input", side_effect=["1"]):
            result, output = self.capture(main.add_product, self.products)
        self.assertFalse(result)
        self.assertIn("already exists", output)
        self.assertEqual(len(self.products), 2)

    def test_search_by_name_case_insensitive(self):
        with patch("builtins.input", side_effect=["mIlK"]):
            result, output = self.capture(main.search_product, self.products)
        self.assertEqual(result[0]["id"], 1)
        self.assertIn("Dairy", output)

    def test_search_missing_product(self):
        with patch("builtins.input", side_effect=["Juice"]):
            result, output = self.capture(main.search_product, self.products)
        self.assertIsNone(result)
        self.assertIn("not found", output)

    def test_stock_add_and_set(self):
        with patch("builtins.input", side_effect=["1", "1", "3"]):
            result, _ = self.capture(main.update_stock, self.products)
        self.assertTrue(result)
        self.assertEqual(self.products[0]["stock"], 8)
        with patch("builtins.input", side_effect=["1", "2", "0"]):
            result, _ = self.capture(main.update_stock, self.products)
        self.assertTrue(result)
        self.assertEqual(self.products[0]["stock"], 0)

    def test_stock_update_missing_id_and_bad_action(self):
        with patch("builtins.input", side_effect=["99"]):
            result, output = self.capture(main.update_stock, self.products)
        self.assertFalse(result)
        self.assertIn("not found", output)
        with patch("builtins.input", side_effect=["1", "9"]):
            result, output = self.capture(main.update_stock, self.products)
        self.assertFalse(result)
        self.assertIn("Invalid stock update option", output)

    def test_sale_success_exact_available_stock(self):
        with patch("builtins.input", side_effect=["1", "5"]):
            result, output = self.capture(main.process_sale, self.products, self.sales)
        self.assertTrue(result)
        self.assertEqual(self.products[0]["stock"], 0)
        self.assertEqual(self.sales[0]["total_amount"], 1250.0)
        self.assertIn("Purchase successful", output)

    def test_sale_exceeds_stock_rejected_without_mutation(self):
        with patch("builtins.input", side_effect=["1", "6"]):
            result, output = self.capture(main.process_sale, self.products, self.sales)
        self.assertFalse(result)
        self.assertEqual(self.products[0]["stock"], 5)
        self.assertEqual(self.sales, [])
        self.assertIn("only 5 unit(s) available", output)

    def test_sale_missing_product_rejected(self):
        with patch("builtins.input", side_effect=["99"]):
            result, output = self.capture(main.process_sale, self.products, self.sales)
        self.assertFalse(result)
        self.assertIn("product not found", output)

    def test_invalid_numeric_inputs_are_retried(self):
        with patch("builtins.input", side_effect=["abc", "0", "4"]):
            value, output = self.capture(main.read_integer, "Number: ")
        self.assertEqual(value, 4)
        self.assertIn("Invalid input", output)
        self.assertIn("at least 1", output)

    def test_price_validation_retries_non_numeric_and_non_positive(self):
        with patch("builtins.input", side_effect=["bad", "0", "12.5"]):
            value, output = self.capture(main.read_price, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("valid number", output)
        self.assertIn("greater than zero", output)

    def test_add_product_retries_blank_text_and_negative_stock(self):
        with patch("builtins.input", side_effect=["3", "", "Eggs", "", "Dairy", "80", "-1", "0"]):
            result, output = self.capture(main.add_product, self.products)
        self.assertTrue(result)
        self.assertEqual(self.products[-1]["name"], "Eggs")
        self.assertEqual(self.products[-1]["stock"], 0)
        self.assertIn("cannot be empty", output)
        self.assertIn("at least 0", output)

    def test_sale_from_zero_stock_is_rejected(self):
        with patch("builtins.input", side_effect=["2", "1"]):
            result, output = self.capture(main.process_sale, self.products, self.sales)
        self.assertFalse(result)
        self.assertIn("only 0 unit(s) available", output)
        self.assertEqual(self.sales, [])

    def test_report_empty_and_normal_inventory(self):
        _, output = self.capture(main.generate_report, self.products, self.sales)
        self.assertIn("Products below 5 units: Bread", output)
        self.assertIn("Highest-priced product: Milk", output)
        _, empty_output = self.capture(main.generate_report, [], [])
        self.assertIn("Highest-priced product: N/A", empty_output)

    def test_invalid_menu_choice_then_exit(self):
        with patch("builtins.input", side_effect=["invalid", "8"]):
            _, output = self.capture(main.main)
        self.assertIn("Invalid menu choice", output)
        self.assertIn("Goodbye", output)

    def test_empty_display_and_sales(self):
        _, products_output = self.capture(main.display_products, [])
        _, sales_output = self.capture(main.view_sales, [])
        self.assertIn("No products", products_output)
        self.assertIn("No sales", sales_output)


if __name__ == "__main__":
    unittest.main()
