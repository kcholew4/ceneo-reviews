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
        return scrapper.get_product_data(product_id)

    def _replace_product(self, product_id, new_product):
        return self.collection.replace_one({"product_id": product_id}, new_product)

    def get_product(self, product_id):
        product = self._find_product(product_id)

        if product != None:
            if product["partial_reviews_data"]:
                print("partial product data")

                product = self._fetch_product(product_id)
                self._replace_product(product_id, product)

            return product

        product = self._fetch_product(product_id)

        if product == None:
            return None

        self._store_product(product)

        del product["_id"]  # pymongo adds _id field
        return product
