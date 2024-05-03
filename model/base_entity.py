from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

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
     
