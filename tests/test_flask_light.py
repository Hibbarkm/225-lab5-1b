import unittest
import sqlite3
import os
from main import app  # your Flask app entry point

DB_PATH = os.path.join("data", "parts.db")  # matches your repo structure

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

    def test_database_has_tables(self):
        """Check that database has at least one table"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        self.assertTrue(len(tables) > 0)

if __name__ == "__main__":
    unittest.main()
