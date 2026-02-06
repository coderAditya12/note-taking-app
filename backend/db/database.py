from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.constant.utlis import database_url

from backend.model.base import Base
if not database_url:
    raise ValueError("DATABASE_URL is not set in environment variables.")

engine = create_engine(database_url)
def init_db():
    from backend.model.notes import Notes
    from backend.model.user import User
    Base.metadata.create_all(engine)

def get_session():
    session = sessionmaker(bind=engine)
    
    return session()

