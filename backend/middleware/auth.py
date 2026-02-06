import jwt
from fastapi import Request, HTTPException, status


async def jwt_auth_middleware(request: Request, call_next):
    if request.url.path in ["/signup", "/login"]:
        return await call_next(request)
    cookies = request.cookies.get("token")
    if not cookies:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please relogin"
        )
