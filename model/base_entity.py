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

class TaskEntity(BaseEntity):
    __tablename__ = "tasks"

    task_id = Column(BIGINT, unique=True,index=True)
    task_name = Column(String)
    task_description = Column(String)


    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False )
    project = relationship("ProjectEntity",back_populates="tasks")

    leader_id = Column(BIGINT,ForeignKey('leaders.id'),nullable=True )
    leader = relationship("LeaderEntity",back_populates="tasks")

    user_id = Column(BIGINT, ForeignKey('users.id'),nullable=True )
    users = relationship("UserEntity", back_populates="tasks")

class ProjectEntity(BaseEntity):
    __tablename__ = "projects"
    
    project_name = Column(String, unique=False , index=True)
    username = Column(String, unique=False, index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    users = relationship("UserEntity",secondary = "userproject",back_populates="projects")
    leaders = relationship("LeaderEntity",back_populates="project")

    tasks = relationship("TaskEntity",back_populates='project')

class ManagerEntity(BaseEntity):
    __tablename__ = "admin"
    
    admin_name = Column(String)
    admin_pass = Column(String)

class LeaderEntity(BaseEntity):
    __tablename__ = "leaders"
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserEntity", back_populates="leaders")
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("ProjectEntity", back_populates="leaders")

    tasks = relationship("TaskEntity",back_populates='leader')


class UserEntity(BaseEntity):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    # gmail = Column(String, unique=True,index=True)
    first_name = Column(String, unique=False, index=True)
    last_name = Column(String, unique=False, index=True)
    hash_password = Column(String)
    projects = relationship("ProjectEntity",secondary = "userproject",back_populates="users")
    leaders = relationship("LeaderEntity",back_populates="user")

    tasks = relationship("TaskEntity",back_populates='users')

class UserProjectEntity(BaseEntity):
    __tablename__ = "userproject"
    user_id = Column(BIGINT,ForeignKey('users.id'),nullable=False)
    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False)

# class TaskEntity(BaseEntity):
#     __tablename__ = "tasks"

#     task_id = Column(String, unique=True,index=True)
#     task_name = Column(String)
#     task_description = Column(String)


#     project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False )
#     project = relationship("ProjectEntity",back_populates="tasks")

#     leader_id = Column(BIGINT,ForeignKey('leaders.id'),nullable=False )
#     leader = relationship("LeaderEntity",back_populates="tasks")

#     user_id = Column(BIGINT, ForeignKey('users.id'),nullable=False )
#     users = relationship("UserEntity", back_populates="tasks")