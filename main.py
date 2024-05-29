from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic, get_credentials_from_database
from logic.project_logic import project
from logic.task_logic import Tasks
import psycopg2
from psycopg2 import OperationalError

engine = create_engine("postgresql://postgres:postgres@localhost/trello")
Base.metadata.create_all(engine)


x=UserLogic()
# x.signup_user()
x.signin_user()
# x.list_tasks()
# x.list_projects()
# x.list_leader_project()

y = project(x)

# y.delete_user_from_project()
# y.delete_project()
# y.list_tasks()
# y.list_users()
# y.create_project()
# y.add_user_to_project()

z = Tasks(y,x)
# z.list_users()
z.create_task()
# z.add_comment_to_task()
# z.add_user_to_task()
# z.list_comment()
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