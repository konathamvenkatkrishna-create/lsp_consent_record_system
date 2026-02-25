# from sqlalchemy import  Column, BigInteger,String, Text
# from app.core.db import Base

# class User(Base):
#     __tablename__ = "users"
 
#     id = Column(BigInteger, primary_key=True)
#     # username = Column(String(50),unique=True)
#     # mobile_number = Column(String(25), unique=True)
#     # password_hash = Column(String)
#     # device_id = Column(Text,nullable=True)
#     # role = Column(String,default="USER")


from sqlalchemy import Column, BigInteger, String, Text
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    mobile_number = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    device_id = Column(Text, nullable=True)
    role = Column(String(20), default="USER", nullable=False)
