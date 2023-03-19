from flask_restful import Resource

from lib.store import Store


class ProductsList(Resource):
    def get(self):
        store = Store()
        return store.get_stored_products(), 200
