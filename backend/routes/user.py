from fastapi import APIRouter, HTTPException, status
from backend.pydantic_model.user import User_data
from backend.db.database import get_session
from sqlalchemy import Select
from backend.model.user import User

router = APIRouter(prefix="users", tags=["user"])


@router.post("/login")
def user_signup(user: User_data):
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
    session.close()
    return {
        "status": status.HTTP_201_CREATED,
        "message": "user created successfull",
        "user ID": new_user.id,
    }
