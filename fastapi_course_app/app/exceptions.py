from fastapi import HTTPException, status


class BookingHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists."


class BookingUnauthorizedException(BookingHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED


class BookingBadRequestException(BookingHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST


class BookingNotFoundException(BookingHTTPException):
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectEmailOrPasswordException(BookingUnauthorizedException):
    detail = "Incorrect email or password."


class NoPasswordException(BookingBadRequestException):
    detail = "Password is not specified."


class TokenExpiredException(BookingUnauthorizedException):
    detail = "Token is expired."


class TokenAbsentException(BookingUnauthorizedException):
    detail = "Token is absent."


class IncorrectTokenFormatException(BookingUnauthorizedException):
    detail = "Incorrect token format."


class UserNotExistsException(BookingUnauthorizedException):
    pass


class RoomCannotBeBookedException(BookingHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "There are no free rooms."


class DateFromBiggerThanDateToException(BookingBadRequestException):
    detail = "Date of ending of booking period cannot be bigger than date of its beginning."


class TooBigDateIntervalException(BookingBadRequestException):
    detail = "Interval between end date and begin date from cannot be more than 30 days."


class HotelNotExistsError(BookingNotFoundException):
    detail = "Hotel not exists."


class RoomNotExistsException(BookingNotFoundException):
    detail = "Room not exists."


class IncorrectTableNameException(BookingBadRequestException):
    detail = "Invalid table name. Possible variants: bookings, hotels, rooms."
