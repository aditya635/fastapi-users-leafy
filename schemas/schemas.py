import uuid
from pydantic import BaseModel
from typing import Optional,List
class File(BaseModel):
    url: str
    caption :str
    id:int
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name:str
    email:str
    images : Optional[List[File]] = []
    class Config():
        orm_mode=True

class User(BaseModel):
    name:str
    email:str
    password:str



class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Caption(BaseModel):
    caption:str
