from pydantic import BaseModel


class SLogin(BaseModel):
    access_token: str
    type: str = "bearer"
