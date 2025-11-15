import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Replace with your deployed ClusterIP service URL
CLUSTER_IP = "http://<YOUR_CLUSTER_IP>:5000"  

class SeleniumLightTests(unittest.TestCase):

    def setUp(self):
        # Use headless mode to prevent opening browser windows during Jenkins build
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(CLUSTER_IP)
        time.sleep(1)  # small wait for page to load

    def test_page_title(self):
        """Check that page title contains 'Parts'"""
        self.assertIn("Parts", self.driver.title)

    def test_parts_table_exists(self):
        """Check that the parts table exists"""
        table = self.driver.find_element(By.ID, "parts-table")  # match your table ID
        self.assertIsNotNone(table)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
