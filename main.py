from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic, get_credentials_from_database
from logic.project_logic import project, project_menu, get_user_credentials
from logic.task_logic import tasks, get_credentials_from_database2
import psycopg2
from psycopg2 import OperationalError

engine = create_engine("postgresql://postgres:foxit@localhost/t2")
Base.metadata.create_all(engine)


# print(get_user_credentials())
x=UserLogic()
x.signin_user()

# print(x.get_id_user_login())
# x.signin_user()
# x.signup_user()
# print(get_credentials_from_database2("tasks"))
y = project(x)
z = tasks(y,x)
z.create_task()

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


    
        #   UPDATING DATABASE CODE
# import psycopg2
# # Connect to the database
# conn = psycopg2.connect(
#     dbname="trello",
#     user="postgres",
#     password="foxit",
#     host="localhost",  # Assuming your local PostgreSQL is running on localhost
#     port="5432"  # Default PostgreSQL port
# )
# cursor = conn.cursor()