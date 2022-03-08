from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

class UserTable(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "users"
    name = Column(String)
    images = relationship("Images",  back_populates="creator")


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String)
    url = Column(URLType)
    user_id = Column(UUID, ForeignKey('users.id'))
    creator = relationship("UserTable", back_populates="images")