from fastapi import HTTPException, status


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"Auth-Token": ""},
            )
        )


class InvalidLogin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
