from flask_restful import Resource

from lib.ceneo.scrapper import Scrapper


class Product(Resource):
    def get(self, id):
        # Check the db first

        scrapper = Scrapper()

        page = scrapper.get_reviews_page(id)

        if page == None:
            return {
                "ok": False,
                "message": "product not found"
            }

        return page.reviews, 200
