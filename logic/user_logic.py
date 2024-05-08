from sqlalchemy import select
from model.base_entity import UserEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
import psycopg2
from tabulate import tabulate

engine = create_engine("postgresql://postgres:foxit@localhost/trello")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class user:
    def __init__(self):
        self.session = get_session()
        self.create_user_from_input()

    def create_user(self, gmail, username, hash_password, first_name, last_name):
        user = self.session.execute(select(UserEntity).filter_by(username=username))
        result_edited = user.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("username is exist")
        else:
            db_model = UserEntity(gmail=gmail, username=username, hash_password=hash_password, first_name=first_name, last_name=last_name)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)

    def create_user_from_input(self):
        gmail, username, hash_password, first_name, last_name = self.prompt_user_info()
        self.create_user(gmail, username, hash_password, first_name, last_name)

    def prompt_user_info(self):
        gmail = input("please enter gmail: ")
        username = input("please enter username : ")
        hash_password = input("please enter password : ")
        first_name = input("please enter first_name : ")
        last_name = input("please enter last_name : ")
        return gmail, username, hash_password, first_name, last_name

def get_credentials_from_database(table_name):
    try:
        # Create a session
        session = get_session()

        # Reflect the table
        metadata = MetaData()
        metadata.reflect(engine)
        table = Table(table_name, metadata, autoload=True)

        # Query the table and fetch all rows
        rows = session.query(table).all()

        # Create a dictionary to store usernames and passwords
        credentials = {row.username: row.hash_password for row in rows}

        # Close the session
        session.close()

        # Return the dictionary of credentials
        return credentials

    except Exception as e:
        print("Error while fetching data from database:", e)
# from sqlalchemy import select, text, update
# from model.base_entity import UserEntity
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

# engine = create_engine("postgresql://postgres:foxit@localhost/trello")

# def get_session():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session

# class user:
#     def __init__(self):
#         # self.password = password
#         # self.username = username
#         # self.validatore()
#         self.session = get_session()

#     def create_user(self,gmail=input("please enter gmail: ") ,username=input("please enter username : "),hash_password = input("please enter password : "),first_name = input("please enter first_name : "),last_name = input("please enter last_name : ")):
#         user = self.session.execute(select(UserEntity).filter_by(username=username))
#         result_edited = user.scalars().one_or_none()
#         print(result_edited)
#         if result_edited:
#             print("username is exist")
#         else:
#             db_model = UserEntity( gmail=gmail,username=username,hash_password=hash_password,first_name=first_name,last_name=last_name)
#             self.session.add(db_model)
#             self.session.commit()
#             self.session.refresh(db_model)
        

#     def check_login_password(self,password):
#         pass

