from pydantic import BaseModel


class User_data(BaseModel):
    name: str
    email: str
    password: str


class User_login(BaseModel):
    email: str
    password: str
