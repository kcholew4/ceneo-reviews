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

        reviews = []

        for userPost in userPosts:
            extract = Extract(userPost)

            reviews.append(Review(
                id=extract.id(),
                author=extract.author(),
                recommendation=extract.recommendation(),
                scoreCount=extract.scoreCount(),
                verified=extract.verified(),
                dates=extract.dates(),
                votes=extract.votes(),
                text=extract.text(),
                features=extract.features()
            ))

        def createResponse(review):
            res = {}

            res["id"] = review.id
            res["author"] = review.author
            res["text"] = review.text
            res["verified"] = review.verified

            return res

        response = []

        for review in reviews:
            response.append(createResponse(review))

        return response, 200
