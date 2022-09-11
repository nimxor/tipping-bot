import models
import error
import wallet


def register_user(user_id: str, user_wallet: str = None) -> models.User:
    dbWallet = wallet.getWallet(user_id)
    if dbWallet is not None:
        if user_wallet:
            wallet.updateWallet(user_id, {"address": user_wallet})
            user_model = models.User(user_id=user_id, actual_address=user_wallet)
            return user_model
        else:
            wallet_address = dbWallet["address"]
            user_model = models.User(user_id=user_id, actual_address=wallet_address)
            return user_model
    else:
        wallet.initNewWallet(user_id, user_wallet)
        user_model = models.User(user_id=user_id, actual_address=user_wallet)
        return user_model


def get_user_wallet(user_id: str) -> models.Wallet:
    dbWallet = wallet.getWallet(user_id)
    if dbWallet is None:
        raise error.WalletNotFoundError
    wallet_model = models.Wallet(dbWallet["address"], dbWallet["tokens"])
    return wallet_model


def add(user: models.User, amount: int) -> models.User:
    dbWallet = wallet.getWallet(user.user_id)
    newAmount = dbWallet["tokens"] + amount
    wallet.updateWallet(user.user_id, {"tokens": newAmount})


def send_tip(user_from: models.User, user_to: models.User, amount: int) -> models.Tip:
    wallet_sender = wallet.getWallet(user_from.user_id)
    wallet_receiver = wallet.getWallet(user_to.user_id)
    if wallet_sender is None or wallet_receiver is None:
        raise error.WalletNotFoundError

    user_from_address = wallet_sender["address"]
    user_to_address = wallet_receiver["address"]

    token_from_address = wallet_sender["tokens"]
    token_to_address = wallet_receiver["tokens"]
    if token_from_address >= amount:
        token_from_address -= amount
        token_to_address += amount
        tip = models.Tip(user_from, user_to, amount)
        wallet.updateWallet(user_from.user_id, {"tokens": token_from_address})
        wallet.updateWallet(user_to.user_id, {"tokens": token_to_address})
        return tip
    else:
        raise error.InsufficientAmountError


# def withdraw(user: models.User, amount: int) -> models.Withdrawal:
#     dbWallet = wallet.getWallet(user.user_id)
#     if dbWallet is None:
#         raise error.WalletNotFoundError
#     tokens = dbWallet["tokens"]
#     wallet.updateWallet(user_to.user_id, {"tokens": tokens})
#     if tokens >= amount:
#         tokens -= amount
#
#     else:
#         raise error.InsufficientAmountError
#     return models.Withdrawal(user, amount)
