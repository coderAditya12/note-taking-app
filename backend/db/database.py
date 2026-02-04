from sqlalchemy import create_engine
from backend.constant.utlis import database_url

if not database_url:
    raise ValueError("DATABASE_URL is not set in environment variables.")

engine = create_engine(database_url)
def main():
    connection =engine.connect()
    print("connected to database",connection)

