from fastapi import APIRouter, HTTPException, status, Response
from backend.pydantic_model.user import User_data
from backend.db.database import get_session
from sqlalchemy import Select
from backend.model.user import User
from backend.constant.utlis import secret
import jwt

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/signup")
def user_signup(user: User_data, response: Response):
    print("users data",user)
    session = get_session()
    name = user.name
    email = user.email
    password = user.password
    if not name or not email or not password:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Please provide the required field",
        )
    stmt = Select(User).where(User.email == email)
    existing_user = session.scalar(stmt)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use.Please login",
        )
    new_user = User(name=user.name, email=user.email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    
  
    
    #use jwt
    encoded_jwt = jwt.encode({"id":str(new_user.id)},secret,algorithm="HS256") # type: ignore
    session.close()
    response.set_cookie(key="token",value=encoded_jwt)
    return {
        "status": status.HTTP_201_CREATED,
        "message": "user created successfull",
        "user ID": str(new_user.id),
    }
