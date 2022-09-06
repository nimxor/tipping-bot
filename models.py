import re
import error

class WalletAddressField:
  def __init__(self, address: str):
    regex = r'addr([0-9]+([a-zA-Z]+[0-9]+)+)'
    patter = re.compile(regex)
    max_length = 200
    if address == None:
      self.address = address
      return
    if patter.match(address) and len(address) <= max_length:
      print("Address LOL")
      self.address = address
    else:
      raise error.AddressSyntexError

class User:
  def __init__(self, user_id: str, actual_address: str, db_address: str):
    self.user_id = user_id
    self.actual_address = WalletAddressField(actual_address)
    self.db_address = db_address

class Wallet:
  def __init__(self, wallet_address: str, balance: int):
    self.wallet_address = WalletAddressField(wallet_address)
    self.balance = balance

class Tip:
  def __init__(self, from_user: User, to_user: User, amount: int):
    self.from_user = from_user
    self.to_user = to_user
    self.amount = amount

class Withdrawal:
  def __init__(self, user: User, amount: int):
    self.user = user
    self.amount = amount

