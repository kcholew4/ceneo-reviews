from flask_restful import Resource

from lib.ceneo.scrapper import Scrapper


class Product(Resource):
    def get(self, id):
        # Check the db first

        scrapper = Scrapper()

        status_code = scrapper.query(
            f"https://www.ceneo.pl/{id}")

        if status_code == 404:
            return {
                "ok": False,
                "message": "product not found"
            }

        product_name = scrapper.product_name()

        if not product_name:
            return {
                "ok": False,
                "message": "limit exceeded"
            }

        reviews = scrapper.reviews()
        reviews_page = scrapper.reviews_page()
        reviews_has_next_page = scrapper.reviews_has_next_page()

        reviews_data = [{
            "page_number": reviews_page,
            "has_next_page": reviews_has_next_page,
            "reviews": reviews
        }]

        partial = False

        while reviews_has_next_page:
            status_code = scrapper.query(
                f"https://www.ceneo.pl/{id}/opinie-{reviews_page + 1}")

            if not scrapper.product_name():
                partial = True
                break  # limit exceeded

            reviews = scrapper.reviews()
            reviews_page = scrapper.reviews_page()
            reviews_has_next_page = scrapper.reviews_has_next_page()

            reviews_data.append({
                "page_number": reviews_page,
                "has_next_page": reviews_has_next_page,
                "reviews": reviews
            })

        return {
            "name": product_name,
            "partial_data": partial,
            "data": reviews_data
        }, 200
