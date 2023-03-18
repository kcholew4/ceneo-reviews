from flask_restful import Resource

from lib.ceneo.scrapper import Scrapper
import db


class Product(Resource):
    def get(self, id):
        scrapper = Scrapper()

        result = scrapper.get_product_data(id)

        if result == None:
            return {
                "ok": False,
                "message": "product not found"
            }, 404

        return result, 200
