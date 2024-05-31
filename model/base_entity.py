from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Enum
from sqlalchemy.orm import Mapped, mapped_column,relationship
import enum
Base = declarative_base()
class StatusEnum(enum.Enum):
    BACKLOG = "BACKLOG"
    DOING = "DOING"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"

class PriorityEnum(enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
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
    status = Column(Enum(StatusEnum), default=StatusEnum.BACKLOG)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.LOW)

    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False )
    project = relationship("ProjectEntity",back_populates="tasks")

    leader_id = Column(BIGINT,ForeignKey('leaders.id'),nullable=True )
    leader = relationship("LeaderEntity",back_populates="tasks")

    # user_id = Column(BIGINT, ForeignKey('users.id'),nullable=True )
    users = relationship("UserEntity",secondary = "usertask",back_populates="tasks")

    comments = relationship("CommentEntity",back_populates='task')
    historys = relationship("Task_History",back_populates='task')

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
    comments = relationship("CommentEntity",back_populates='project')

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

    tasks = relationship("TaskEntity",secondary = "usertask",back_populates="users")
    comments = relationship("CommentEntity",back_populates='user')
    
class UserProjectEntity(BaseEntity):
    __tablename__ = "userproject"
    user_id = Column(BIGINT,ForeignKey('users.id'),nullable=False)
    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False)

class CommentEntity(BaseEntity):
    __tablename__ = "comments"

    comment_name = Column(String)

    task_id = Column(BIGINT,ForeignKey('tasks.id'),nullable=False )
    task = relationship("TaskEntity",back_populates="comments")

    project_id = Column(BIGINT,ForeignKey('projects.id'),nullable=False )
    project = relationship("ProjectEntity",back_populates="comments")

    user_id = Column(BIGINT, ForeignKey('users.id'),nullable=True )
    user = relationship("UserEntity", back_populates="comments")

class UserTaskEntity(BaseEntity):
    __tablename__ = "usertask"
    user_id = Column(BIGINT,ForeignKey('users.id'),nullable=False)
    task_id = Column(BIGINT,ForeignKey('tasks.id'),nullable=False)

class Task_History(BaseEntity):
    __tablename__ = "historis"

    task_id = Column(BIGINT,ForeignKey('tasks.id'),nullable=False )
    task = relationship("TaskEntity",back_populates="historys")
    edit_status = Column(Enum(StatusEnum))
    edit_priority = Column(Enum(PriorityEnum))
    edit_description = Column(String)
    username = Column(String)