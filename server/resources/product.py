from flask_restful import Resource
from bs4 import BeautifulSoup
import requests

from lib.extract import Extract
from lib.review import Review


class Product(Resource):
    def get(self, id):
        r = requests.get(f"https://www.ceneo.pl/{id}")

        soup = BeautifulSoup(r.text, features="html.parser")

        userPosts = soup.select(
            "div.user-post.user-post__card.js_product-review")

        if (len(userPosts) == 0):
            return {
                "ok": False,
                "message": "product not found"
            }, 404

        for userPost in userPosts:
            extract = Extract(userPost)

            review = Review(
                id=extract.id(),
                author=extract.author(),
                recommendation=extract.recommendation(),
                scoreCount=extract.scoreCount(),
                verified=extract.verified(),
                dates=extract.dates(),
                votes=extract.votes(),
                text=extract.text(),
                features=extract.features()
            )

            print(review)

        return {"Hello": "world"}
