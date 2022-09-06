import models
import error
import wallet
from replit import db

def register_user(user_id: str, user_wallet: str = None) -> models.User:
  db_address = wallet.getAddressIdentifier(user_id)
  token_address = wallet.getTokenIdentifier(db_address)
  print(user_wallet)
  if wallet.checkAddressIdentifier(user_id):
    if not user_wallet:
      wallet_address = db[wallet.getAddressIdentifier(user_id)]
      user_model = models.User(user_id=user_id, actual_address=wallet_address,
                             db_address=wallet.getAddressIdentifier(user_id))
      return user_model
    else:
      db[wallet.getAddressIdentifier(user_id)] = user_wallet
      wallet_address = db[wallet.getAddressIdentifier(user_id)]
      user_model = models.User(user_id=user_id, actual_address=wallet_address,
                             db_address=wallet.getAddressIdentifier(user_id))
      
      return user_model
  db[db_address] = user_wallet
  db[token_address] = 0
  user_model = models.User(user_id=user_id, actual_address=user_wallet,
                           db_address=db_address)
  return user_model

def get_user_wallet(user_id: str) -> models.Wallet:
  if not wallet.checkAddressIdentifier(user_id):
    raise error.WalletNotFoundError
  db_address = wallet.getAddressIdentifier(user_id)
  token_address = wallet.getTokenIdentifier(db_address)
  wallet_model = models.Wallet(db[db_address], db[token_address])
  return wallet_model

def add(user: models.User, amount: int) -> models.User:
  user_address = wallet.getAddressIdentifier(user.user_id)
  token_address = wallet.getTokenIdentifier(user_address)
  db[token_address] += amount

def send_tip(user_from: models.User, user_to: models.User, amount: int) -> models.Tip:
  if not wallet.checkAddressIdentifier(user_from.user_id):
    raise error.WalletNotFoundError
  if not wallet.checkAddressIdentifier(user_to.user_id):
    raise error.WalletNotFoundError  
  
  user_from_address = wallet.getAddressIdentifier(user_from.user_id)
  user_to_address = wallet.getAddressIdentifier(user_to.user_id)

  if not wallet.checkTokenIdentifier(user_from_address):
    raise error.TokenNotFoundError
  if not wallet.checkTokenIdentifier(user_to_address):
    raise error.TokenNotFoundError  
  
  token_from_address = wallet.getTokenIdentifier(user_from_address)
  token_to_address = wallet.getTokenIdentifier(user_to_address)
  if db[token_from_address] >= amount:
    db[token_from_address] -= amount
    db[token_to_address] += amount
    tip = models.Tip(user_from, user_to, amount)
    return tip
  else:
    raise error.InsufficientAmountError

def withdraw(user: models.User, amount: int) -> models.Withdrawal:
  if not wallet.checkAddressIdentifier(user.user_id):
    raise error.WalletNotFoundError
  db_address = wallet.getAddressIdentifier(user.user_id)
  if not wallet.checkTokenIdentifier(db_address):
    raise error.TokenNotFoundError
  db_token = wallet.getTokenIdentifier(db_address)
  if db[db_token] >= amount:
    db[db_token] -= amount
  else:
    raise error.InsufficientAmountError
  return models.Withdrawal(user, amount)

