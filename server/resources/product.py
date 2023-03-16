from flask_restful import Resource

from lib.ceneo.scrapper import Scrapper


class Product(Resource):
    def get(self, id):
        # Check the db first

        scrapper = Scrapper(f"https://www.ceneo.pl/{id}")

        if scrapper.status_code() == 404:
            return {
                "ok": False,
                "message": "product not found"
            }

        reviews = scrapper.get_reviews()

        return reviews, 200
