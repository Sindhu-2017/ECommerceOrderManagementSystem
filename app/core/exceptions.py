class AppError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DuplicateEmailError(AppError):
    pass


class DuplicateUsernameError(AppError):
    pass


class DuplicatePhoneError(AppError):
    pass


class InvalidCredentialsError(AppError):
    pass


class InactiveUserError(AppError):
    pass


class InvalidTokenError(AppError):
    pass


class RefreshTokenNotFoundError(AppError):
    pass


class DatabaseOperationError(AppError):
    pass


class CategoryNotFoundError(AppError):
    pass


class CategoryAlreadyExistsError(AppError):
    pass


class ProductNotFoundError(AppError):
    pass


class ProductAlreadyExistsError(AppError):
    pass


class InvalidProductDataError(AppError):
    pass


class OrderNotFoundError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class InvalidOrderOperationError(Exception):
    pass


class ShippingInUseError(Exception):
    pass
