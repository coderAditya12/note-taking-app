from fastapi import APIRouter, HTTPException, status, Response, Depends
from backend.pydantic_model.user import User_data, User_login
from backend.db.database import get_session
from sqlalchemy import Select
from sqlalchemy.orm import Session
from backend.model.user import User
from backend.constant.utlis import secret
import jwt

if not secret:
    raise ValueError("Secret key is not configured")

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/signup")
def user_signup(
    user: User_data, response: Response, session: Session = Depends(get_session)
):
    print("users data", user)

    name = user.name
    email = user.email
    password = user.password
    if not name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Please provide the required field",
        )
    stmt = Select(User).where(User.email == email)
    existing_user = session.scalars(stmt).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use.Please login",
        )
    new_user = User(name=user.name, email=user.email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    # use jwt
    encoded_jwt = jwt.encode({"id": str(new_user.id)}, secret, algorithm="HS256")  
    session.close()
    response.set_cookie(key="token", value=encoded_jwt)
    return {
        "status": status.HTTP_201_CREATED,
        "message": "user created successfull",
        "user ID": str(new_user.id),
    }


@router.post("/login")
def user_login(
    user: User_login, response: Response, session: Session = Depends(get_session)
):
    user_email = user.email
    user_password = user.password
    if not all([user_email, user_password]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Please provide correct email and password",
        )
    stmt = Select(User).where(User.email == user_email)
    existing_user = session.scalars(stmt).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email is not present"
        )
    print("existing User in login", existing_user)
    password_check = existing_user.check_password(user_password)  
    if not password_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect"
        )
    encoded_jwt = jwt.encode({"id": str(existing_user.id)}, secret, algorithm="HS256")  # type: ignore
    response.set_cookie(key="token", value=encoded_jwt)
    return {"status": status.HTTP_200_OK, "message": "Login successfull"}
