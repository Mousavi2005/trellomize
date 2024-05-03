from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from .base_entity import BaseEntity
from .project_entity import ProjectEntity

class UserEntity(BaseEntity):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    projects = relationship("ProjectEntity",secondary = "user-project",back_populates="users")
    leaders = relationship("LeaderEntity",back_populates="user")