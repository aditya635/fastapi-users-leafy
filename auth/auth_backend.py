from fastapi_users.authentication import JWTStrategy,AuthenticationBackend, CookieTransport
from dotenv import load_dotenv
load_dotenv()
import os 



SECRET = os.environ["SECRET"]


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

cookie_transport = CookieTransport(cookie_max_age=3600)

auth_back = AuthenticationBackend(
    name= "jwt",
    transport = cookie_transport,
    get_strategy=get_jwt_strategy,
)



