from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from .base_entity import BaseEntity


class LeaderEntity(BaseEntity):
    __tablename__ = "leaders"
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserEntity", back_populates="leaders")
    project_id = Column(Integer, ForeignKey('prpjects.id'))
    project = relationship("ProjectEntity", back_populates="leaders")
