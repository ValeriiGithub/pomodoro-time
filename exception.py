class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"

class TokenExpired(Exception):
    detail = "Token expired"

class TocenNotCorrect(Exception):
    detail = "Token is not correct"
