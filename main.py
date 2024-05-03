from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
import rich

engine = create_engine('postgresql://postgres:postgres@localhost/trello')

Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



class user:
    def __init__(self,password,user_name):
        self.password = password
        self.user_name = user_name

    def display_info():
        print(f"user_name : {user_name}  passwprd : {password}")

    def get_password_for_new_account():
        password = input("Enter password: ")
        if len(password) < 8 :
            print("Your password must have at least 8 characters")
        # here we have to check if password is reapeted
        # if not add it to database

    def check_login_password(password):
        pass
        # here we have to check if password is in database
    
    def get_username_for_new_account():
        username = input("User name : ")
        if len(username) <=3 :
            print("Your user name must have atleat 4 charachters")
        # here we have to check if username is in database
        # if not add it to database
    

        





    
class admin_user(user):
    def __init__(self,password,user_name,gmail):
        super().__init__(password,user_name)
        self.gmail = gmail

    def display_info():
        print(f"user_name : {user_name}  passwprd : {password}  gmail : {gmail}")

    


    