from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String
from bcrypt import gensalt,hashpw,checkpw
from  uuid import uuid4,UUID
class User(DeclarativeBase):
    __tablename__="user"
    id:Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(50))
    email:Mapped[str]=mapped_column(String(120),unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    
    def set_password(self,password:str):
        passowrd_in_bytes = password.encode('utf-8')
        print("password in bytes")
        self.password= hashpw(passowrd_in_bytes,gensalt()).decode()
        print("password decoding", self.password)
    def check_password(self,password:str)->bool:
        return checkpw(password.encode(),self.password.encode('utf-8'))
        
        