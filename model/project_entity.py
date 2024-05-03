from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from .base_entity import BaseEntity
from .user_entity import UserEntity

class ProjectEntity(BaseEntity):
    __tablename__ = "projects"
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    users = relationship("UserEntity",secondary = "user-project",back_populates="projects")
    leaders = relationship("LeaderEntity",back_populates="project")
