from flask_restful import Resource
import requests

class Check(Resource):
  def get(self, id):
    r = requests.get(f"https://ceneo.pl/{id}")

    if (r.status_code == 404):
      return { "exists": False }, 404

    if (r.status_code == 200):
      return { "exists": True }, 200

    return { "ok": False }, 500
    