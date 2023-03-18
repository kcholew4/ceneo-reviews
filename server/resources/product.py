from flask_restful import Resource

from lib.ceneo.scrapper import Scrapper
from db import db


class Product(Resource):
    def get(self, id):
        products_collection = db["products"]

        product = products_collection.find_one({
            "product_id": id
        }, {"_id": 0})

        if product != None:
            print("getting data from the db")
            return product, 200

        scrapper = Scrapper()

        result = scrapper.get_product_data(id)

        if result == None:
            return {
                "ok": False,
                "message": "product not found"
            }, 404

        products_collection.insert_one(result)

        return result, 200
