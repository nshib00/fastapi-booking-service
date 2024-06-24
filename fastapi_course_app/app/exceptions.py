from fastapi import HTTPException, status


class BookingHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists.'


class BookingUnauthorizedException(BookingHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED


class IncorrectEmailOrPasswordException(BookingUnauthorizedException):
    detail = 'Incorrect email or password.'


class TokenExpiredException(BookingUnauthorizedException):
    detail = 'Token is expired.'


class TokenAbsentException(BookingUnauthorizedException):
    detail = 'Token is absent.'


class IncorrectTokenFormatException(BookingUnauthorizedException):
    detail = 'Incorrect token format.'


class UserNotExistsException(BookingUnauthorizedException):
    pass


class RoomCannotBeBookedException(BookingHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'There are no free rooms.'
