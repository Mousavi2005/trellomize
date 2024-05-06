# from ..main import get_session
from sqlalchemy import select, text, update
from model.base_entity import UserEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

engine = create_engine("postgresql://postgres:postgres@localhost/trello")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class user:
    def __init__(self):
        # self.password = password
        # self.username = username
        # self.validatore()
        self.session = get_session()

    def create_user(self,username=input("please enter username : "),hash_password = input("please enter password : "),first_name = input("please enter first_name : "),last_name = input("please enter last_name : ")):
        user = self.session.execute(select(UserEntity).filter_by(username=username))
        result_edited = user.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("username is exist")
        else:
            db_model = UserEntity(username=username,hash_password=hash_password,first_name=first_name,last_name=last_name)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)
            
    # def display_info(self):
    #     try:
    #         if self.validatore():
    #             print(f"user_name : {self.username}  passwprd : {self.password}")
    #         else:
    #             raise Exception("Value Error")
    #     except Exception as e:
    #         print(e)
    # def validatore(self):
    #     try:
    #         if len(self.password) <= 8 :
    #             raise Exception("Your password must have at least 8 characters")
    #         if len(self.username) <=4 :
    #             raise Exception("Your user name must have atleat 4 charachters")
    #     except  Exception as e:
    #         print(e)
    # def get_password_for_new_account(self):
    #     try:
    #         if len(self.password) <= 8 :
    #             raise Exception("Your password must have at least 8 characters")
    #     except Exception as e:
    #         print(e)

        # here we have to check if password is reapeted
        # if not add it to database

    def check_login_password(self,password):
        pass
        # here we have to check if password is in database
    
    # def get_username_for_new_account(self):
    #     try:
    #         if len(self.username) <=4 :
    #             raise Exception("Your user name must have atleat 4 charachters")
    #     except Exception as e:
    #             print(e)
            # here we have to check if username is in database
            # if not add it to database
# x = user()
# print(x.display_info())