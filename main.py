from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import user
engine = create_engine("postgresql://postgres:postgres@localhost/trello")

Base.metadata.create_all(engine)


x=user()
x.create_user()

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
