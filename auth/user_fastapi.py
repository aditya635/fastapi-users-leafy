from schemas.user_schemas import UserDB,UserCreate,UserUpdate,User
from utils.user_manager import get_user_manager
from database.database import create_db_and_tables
from fastapi_users import FastAPIUsers
from auth.auth_backend import auth_back

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_back],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
current_user = fastapi_users.current_user()
