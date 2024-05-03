from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from .base_entity import BaseEntity
from .project_entity import ProjectEntity

class UserProjectEntity(BaseEntity):
    __tablename__ = "user-project"
    user_id = Column(BIGINT,ForeignKey('users.id'),nullable=False)
    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False)