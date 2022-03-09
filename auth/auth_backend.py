from fastapi_users.authentication import JWTStrategy,AuthenticationBackend, CookieTransport,BearerTransport
from dotenv import load_dotenv
load_dotenv()
import os 



SECRET = os.environ["SECRET"]


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_back = AuthenticationBackend(
    name= "jwt",
    transport = bearer_transport,
    get_strategy=get_jwt_strategy,
)



