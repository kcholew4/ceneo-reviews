from flask import Flask
from flask_restful import Api

from resources.product import Product

app = Flask(__name__)
api = Api(app)


api.add_resource(Product, "/api/products/<id>")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
