import argparse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import user
from logic.project_logic import project
from logic.manager_logic import manager
engine = create_engine("postgresql://postgres:foxit@localhost/trello")

Base.metadata.create_all(engine)



x = manager()

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session










#           UPDATING DATABASE CODE
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

# # Drop all tables
# drop_tables_query = """
#     DROP SCHEMA public CASCADE;
#     CREATE SCHEMA public;
# """
# cursor.execute(drop_tables_query)

# # Commit the transaction
# conn.commit()

# # Close the connection
# conn.close()
