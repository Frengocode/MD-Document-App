from fastapi import HTTPException


class ShortPasswordException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Password should have 8 characters !")


class RoleException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Role should be Cheker !")


class ExistUserException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=400, detail="User with this username all ready was used  !"
        )


class UserNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="User not found !")


class InCorrectPasswordException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="InCorrect password")
