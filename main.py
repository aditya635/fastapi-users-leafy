import imp
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from schemas.user_schemas import UserDB,UserCreate,UserUpdate,User
from utils.user_manager import get_user_manager
from database.database import create_db_and_tables
from auth.user_fastapi import fastapi_users,current_user
from auth.auth_backend import auth_back
from ml import model_ini
from routers import files

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_back),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_user)):
    return {"message": f"Hello {user.email}!"}

app.include_router(
    files.router
)

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()