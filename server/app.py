from flask import Flask
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
api = Api(app)


class Product(Resource):
    def get(self, id):
        # Check if the product is already in the database
        # if yes, query the db and simply return the reviews. Otherwise scrape
        # them of the website and save them.

        # Reviews are paginated, so they are saved according to the page
        # they were on. (i.e. opinie-2, opinie-3...)
        r = requests.get(f"https://www.ceneo.pl/{id}")

        soup = BeautifulSoup(r.text)

        return {"Hello": "world"}


api.add_resource(Product, "/api/products/<id>")

if __name__ == "__main__":
    app.run(debug=True)
