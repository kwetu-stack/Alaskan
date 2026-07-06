import os
import unittest

from app import create_app
from models.product import Product


class StartupSeedTestCase(unittest.TestCase):
    def setUp(self):
        self.previous_database_url = os.environ.get("DATABASE_URL")
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        if self.previous_database_url is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = self.previous_database_url

    def test_startup_seeds_products_from_master_workbook(self):
        self.assertGreater(Product.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
