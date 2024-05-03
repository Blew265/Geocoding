from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Cordinates(Base):
    __tablename__ = "cordinates"
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)    


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
