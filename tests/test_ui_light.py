import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

# Automatically select URL based on environment variable
ENV = os.environ.get("ENVIRONMENT", "dev").lower()

if ENV == "prod":
    CLUSTER_IP = "http://10.48.229.55"  # Production LoadBalancer IP
else:
    # Dev environment with port-forwarding
    CLUSTER_IP = "http://127.0.0.1:5000"  # Default dev ClusterIP via port-forward

class SeleniumLightTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup Firefox WebDriver once for all tests
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.implicitly_wait(3)  # wait for elements to appear
        cls.driver.get(CLUSTER_IP)
        time.sleep(1)  # small wait for page load

    def test_page_title(self):
        """Check that page title contains 'Parts' or 'Inventory'"""
        self.assertIn("Parts", self.driver.title)

    def test_parts_table_exists(self):
        """Check that the parts table exists"""
        # Use table class or table container as ID
        table_found = False
        try:
            table = self.driver.find_element(By.ID, "rows")
            table_found = True
        except:
            table_found = False
        self.assertTrue(table_found, "Parts table not found on page")

    def test_sample_part_exists(self):
        """Optional: Check that at least one known sample part exists"""
        page_source = self.driver.page_source
        sample_parts = ["Brake Pad", "Oil Filter", "Tire"]
        found = any(p in page_source for p in sample_parts)
        self.assertTrue(found, "No sample parts found on the page")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
