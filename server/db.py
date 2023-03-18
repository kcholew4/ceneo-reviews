from dotenv import load_dotenv
from os import environ
from pymongo import MongoClient

load_dotenv()

connection_string = environ["MONGO_DB_CONNECTION_STRING"]
client = MongoClient(connection_string)
ceneo_db = client["ceneo"]
