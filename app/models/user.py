from sqlalchemy import Column, Integer, String
from app.core.db import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mobile = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
