from fastapi_users import models



class User(models.BaseUser):
    name:str


class UserCreate(models.BaseUserCreate):
    name:str


class UserUpdate(models.BaseUserUpdate):
    name:str


class UserDB(User, models.BaseUserDB):
    
    class Config:
        arbitrary_types_allowed = True




