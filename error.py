# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class InsufficientAmountError(Error):
    """Raised when the input value is too small"""
    pass


class WalletNotFoundError(Error):
    """Raised when the input value is too small"""
    pass


class TokenNotFoundError(Error):
    """Raised when the input value is too small"""
    pass


class AddressSyntexError(Error):
    """Raised when the input value is too small"""
    pass
