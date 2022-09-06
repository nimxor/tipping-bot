from replit import db

def getAddressIdentifier(userID: str) -> str:
  return "{0}address".format(userID)

def getTokenIdentifier(address: str) -> str:
  addr = address.replace("address", "")
  return "{0}token".format(addr)

def checkAddressIdentifier(userID: str) -> str:
  return "{0}address".format(userID) in db.keys()

def checkTokenIdentifier(address: str) -> str:
  addr = address.replace("address", "")
  return "{0}token".format(addr) in db.keys()
