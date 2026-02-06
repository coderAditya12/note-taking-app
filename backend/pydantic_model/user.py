from pydantic import BaseModel
class User_data(BaseModel):
    name:str
    email:str
    password:str
