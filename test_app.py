import unittest
from fastapi.testclient import TestClient
from main import app  
import pandas as pd
import os
from decimal import Decimal
from datetime import datetime

client = TestClient(app)

class TestStockAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up any necessary test files or configurations."""
        data = {
            "datetime": pd.date_range(start="2024-02-01", periods=210, freq='D'),
            "close": [100 + i*0.5 for i in range(210)]
        }
        df = pd.DataFrame(data)
        df.to_csv("HINDALCO_1D.csv", index=False)

    @classmethod
    def tearDownClass(cls):
        """Clean up any test files after testing."""
        if os.path.exists("HINDALCO_1D.csv"):
            os.remove("HINDALCO_1D.csv")

    def test_create_stock_data_valid(self):
        """Test if stock data creation works with valid input."""
        response = client.post("/data", json={
            "timestamp": "2024-02-19T10:30:00",
            "open": 100.50,
            "high": 105.75,
            "low": 98.25,
            "close": 103.00,
            "volume": 10000
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_create_stock_data_invalid(self):
        """Test input validation for incorrect stock data."""
        invalid_data = [
            {"timestamp": "2024-02-19T10:30:00", "open": -100, "high": 105.75, "low": 98.25, "close": 103.00, "volume": 10000},  # Open price negative
            {"timestamp": "2024-02-19T10:30:00", "open": 100.50, "high": 97, "low": 98.25, "close": 103.00, "volume": 10000},  # High lower than low
            {"timestamp": "2024-02-19T10:30:00", "open": 100.50, "high": 105.75, "low": 98.25, "close": "invalid", "volume": 10000},  # Close is string
            {"timestamp": "2024-02-19T10:30:00", "open": 100.50, "high": 105.75, "low": 98.25, "close": 103.00, "volume": -500}  # Negative volume
        ]

        for data in invalid_data:
            response = client.post("/data", json=data)
            self.assertEqual(response.status_code, 422)  # Expect validation error

    def test_get_all_data(self):
        """Test retrieving stock data with pagination."""
        response = client.get("/data?limit=10&offset=0")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_moving_average_calculation(self):
        """Test if moving averages (SMA50 & SMA200) are correctly computed."""
        response = client.get("/strategy/performance")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("total_returns", data)
        self.assertIn("accuracy", data)
        self.assertIn("buy_signals", data)
        self.assertIn("sell_signals", data)

        # Check types
        self.assertIsInstance(data["total_returns"], float)
        self.assertIsInstance(data["accuracy"], float)
        self.assertIsInstance(data["buy_signals"], list)
        self.assertIsInstance(data["sell_signals"], list)

    def test_strategy_performance_file_missing(self):
        """Test handling of missing strategy performance CSV."""
        os.remove("HINDALCO_1D.csv")
        response = client.get("/strategy/performance")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "CSV file not found")

    def test_strategy_performance_invalid_file(self):
        """Test handling of an invalid CSV format."""
        with open("HINDALCO_1D.csv", "w") as f:
            f.write("invalid,data,here\n1,2,3")
        response = client.get("/strategy/performance")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid CSV file format")


if __name__ == "__main__":
    unittest.main()
