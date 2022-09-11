from db import _MongoDBService

client = _MongoDBService()


def getWallet(userID: str) -> dict:
    return client.getCollection().find_one({"discordId": userID})


def updateWallet(userID: str, changeset: dict) -> dict:
    return client.getCollection().update_one({"discordId": userID}, {"$set": changeset})


def initNewWallet(userID: str, addr: str) -> dict:
    return client.getCollection().insert_one({"discordId": userID, "tokens": 0, "address": addr})
