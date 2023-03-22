from db import ceneo_db
from lib.ceneo.scrapper import Scrapper


class Store:
    def __init__(self):
        self.collection = ceneo_db["products"]

    def _find_product(self, product_id):
        return self.collection.find_one({
            "product_id": product_id
        }, {"_id": False})

    def _store_product(self, product):
        return self.collection.insert_one(product)

    def _fetch_product(self, product_id):
        scrapper = Scrapper()
        fetched_product = scrapper.get_product(product_id)

        if not fetched_product:
            return None

        return fetched_product.get()

    def _replace_product(self, product_id, new_product):
        return self.collection.replace_one({"product_id": product_id}, new_product)

    def get_product(self, product_id):
        product = self._find_product(product_id)

        if product != None:
            print("getting product from the db")
            if product["partial_data"]:
                print("partial product data")

                product = self._fetch_product(product_id)
                self._replace_product(product_id, product)

            return product

        product = self._fetch_product(product_id)

        if product == None:
            return None

        # Product found but is protected with captcha
        if product["name"] == None:
            return 2  # Ugly fix

        self._store_product(product)

        del product["_id"]  # pymongo adds _id field
        return product

    def get_stored_products(self):
        result = self.collection.find({}, {"_id": False, "reviews": False})
        return list(result)
