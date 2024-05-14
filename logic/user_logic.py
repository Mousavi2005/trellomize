# from ..main import get_session
from sqlalchemy import select, text, update, MetaData, Table
from model.base_entity import UserEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey


engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class UserLogic:
    def __init__(self):
        self.username = None
        self.hash_password = None
        self.first_name = None
        self.last_name = None
        self.id = None
        self.session = get_session()

    def signup_user(self):
        self.input_user_signup()
        user = self.session.execute(select(UserEntity).filter_by(username=self.username))
        result_edited = user.scalars().one_or_none()
        try:
            if result_edited:
                raise Exception("username is exist. please choise other username")
            else:
                db_model = UserEntity(username=self.username,hash_password=self.hash_password,first_name=self.first_name,last_name=self.last_name)
                self.session.add(db_model)
                self.session.commit()
                self.session.refresh(db_model)
                print("signup successfully")
        except Exception as e:
            print(e)
        
    def signin_user(self):
        self.input_user_signin()
        user = self.session.execute(select(UserEntity).filter_by(username=self.username))
        result_edited = user.scalars().one_or_none()
        try:
            if result_edited:
                if self.hash_password!=result_edited.hash_password:
                    print("-----")
                    print(self.hash_password)
                    print(result_edited.hash_password)
                    raise Exception("password is false")
                else:
                    print("login successfully")
                    self.id=result_edited.id
            else:
                raise Exception("you should signup. username dose not exist")
        except Exception as e:
            print(e)

    def signout(self):
        print("signout successfully")
        self.id = None

    def input_user_signup(self):
        self.username=input("please enter username : ")
        self.first_name = input("please enter first_name : ")
        self.last_name = input("please enter last_name : ")
        self.hash_password = input("please enter password : ")
        
    
    def input_user_signin(self):
        self.username=input("please enter username : ")
        self.hash_password= input("please enter password : ")

    def get_id_user_login(self):
        return self.id


def get_credentials_from_database(table_name):
    try:
        session = get_session()
        credentials = session.query(UserEntity).all()
        for user in credentials:
            print(f"Username: {user.username}, Password: {user.hash_password}")

    # Close the session
        session.close()
    except Exception as e:
        print("Error while fetching data from database:", e)

# def get_user_credentials():
#     try:
#         # Create engine and session
#         eengine = create_engine("postgresql://postgres:foxit@localhost/t2")
#         Session = sessionmaker(bind=engine)
#         session = Session()

#         # Query to fetch usernames and passwords
#         projects = session.query(ProjectEntity).all()

#         # Close the session
#         session.close()

#         # Convert to dictionary
#         credentials = {p.project_name: p.user_name for p in projects}
#         return credentials
#     except Exception as e:
#         print("Error while fetching data from database:", e)

       
    
    