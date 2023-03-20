from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.product import Product
from resources.products_list import ProductsList
from resources.check import Check

app = Flask(__name__)
api = Api(app, catch_all_404s=True)
CORS(app)

api.add_resource(Product, "/api/products/<id>")
api.add_resource(Check, "/api/products/<id>/check")
api.add_resource(ProductsList, "/api/products")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
