from flask_restful import Resource

from lib.store import Store


class Product(Resource):
    def get(self, id):
        if not id.isnumeric():
            return {
                "ok": False,
                "message": "bad request"
            }, 400

        store = Store()

        product = store.get_product(id)

        if product == None:
            return {
                "ok": False,
                "message": "product not found"
            }, 404

        if product == 2:
            return {
                "ok": False,
                "message": "product protected with captcha"
            }, 503

        return product, 200
