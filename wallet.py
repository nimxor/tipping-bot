import db


def getWallet(userID: str) -> dict:
    return db.getCollection().find_one({"discordId": userID})


def updateWallet(userID: str, changeset: dict) -> dict:
    return db.getCollection().update_one({"discordId": userID}, {"$set": changeset})


def initNewWallet(userID: str, addr: str) -> dict:
    return db.getCollection().insert_one({"discordId": userID, "tokens": 0, "address": addr})
