import unittest
import sqlite3
import os
from main import app  # Flask app entry point

DB_PATH = '/nfs/demo.db'  # Updated to match your Flask app

class FlaskLightTests(unittest.TestCase):

    def setUp(self):
        # Flask test client
        self.client = app.test_client()

    def test_index_page_loads(self):
        """Check that index page returns status 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_database_exists(self):
        """Check that the SQLite database exists"""
        self.assertTrue(os.path.exists(DB_PATH))

    def test_parts_table_exists(self):
        """Check that the parts table exists in the database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parts';")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table, "Parts table does not exist in the database")

if __name__ == "__main__":
    unittest.main()
