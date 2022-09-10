from pymongo import MongoClient
import pymongo
import os


def getCollection():
    username = os.environ['MONGODB_USERNAME']
    password = os.environ['MONGODB_PASSWORD']
    # CONNECTION_STRING = "mongodb://{0}:{1}@tipping-bot-db:27017".format(username, password)
    CONNECTION_STRING = "mongodb+srv://{0}:{1}@cluster0.mtyoupg.mongodb.net/?retryWrites=true&w=majority".format(username, password)
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)
    db = client['bison_db']
    return db["token_collection"]