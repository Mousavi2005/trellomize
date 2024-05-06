from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    
    id:Mapped[int] = Column(BigInteger, primary_key=True)
    created_at:Mapped[datetime] = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by:Mapped[int]= Column(BigInteger, nullable=True)
    updated_at:Mapped[datetime] = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_by:Mapped[int] = Column(BigInteger, nullable=True)
    is_deleted:Mapped[bool] = Column(Boolean, nullable=True, default=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)

class ProjectEntity(BaseEntity):
    __tablename__ = "projects"
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    users = relationship("UserEntity",secondary = "userproject",back_populates="projects")
    leaders = relationship("LeaderEntity",back_populates="project")

class LeaderEntity(BaseEntity):
    __tablename__ = "leaders"
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserEntity", back_populates="leaders")
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("ProjectEntity", back_populates="leaders")

class UserEntity(BaseEntity):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    projects = relationship("ProjectEntity",secondary = "userproject",back_populates="users")
    leaders = relationship("LeaderEntity",back_populates="user")

class UserProjectEntity(BaseEntity):
    __tablename__ = "userproject"
    user_id = Column(BIGINT,ForeignKey('users.id'),nullable=False)
    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False)