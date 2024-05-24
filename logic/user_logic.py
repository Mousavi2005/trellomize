# from ..main import get_session
from sqlalchemy import select, text, update, MetaData, Table
from model.base_entity import UserEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import regex as re


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


    def signup_user(self,username, password):
        temdictionary = get_credentials_from_database('users')
        k = 0
        for key, value in temdictionary.items():
            if key == username:
                k = 1

<<<<<<< Updated upstream
        # session = SessionLocal()
        if k == 0 :
            new_user = UserEntity(username=username, hash_password=password)
=======
        gmail_dictionary = get_credentials_from_database_gmail('users')
        t = 0
        for key, value in gmail_dictionary.items():
            if value == gmail:
                t = 1
        

        is_valid_gmail = self.is_gmail(gmail)
        if k == 0 and is_valid_gmail and t == 0:
            new_user = UserEntity(username=username, gmail=gmail , hash_password=password)
>>>>>>> Stashed changes
            try:
                self.session.add(new_user)
                self.session.commit()
                return True
            except InterruptedError:
                self.session.rollback()
                print("error!!!!!!!!!!!")
                return False
            finally:
                self.session.close()
                return True
        elif not is_valid_gmail:
            return "NVG"
        
        elif t == 1 :
            return "UG"

        else : 
            return False


    def login_user(self,username, password):
<<<<<<< Updated upstream
        # session = SessionLocal()
        user = self.session.execute(select(UserEntity).where(UserEntity.username == username, UserEntity.hash_password == password))
        result_edited = user.scalars().one_or_none()
        self.id = result_edited.id
        self.session.close()
        return user
=======

        session = get_session()
        admin = session.execute(select(ManagerEntity).where(ManagerEntity.admin_name == username, ManagerEntity.admin_pass == password))
        result_edited = admin.scalars().one_or_none()
        
        if result_edited != None :
            return "Admin"


        temp_active = get_is_active(username)
        user = self.session.execute(select(UserEntity).where(UserEntity.username == username, UserEntity.hash_password == password))
        result_edited = user.scalars().one_or_none()

        if result_edited == None :
            return False
        elif not temp_active:
            return "NA"
        else:
            # result_edited = user.scalars().one_or_none()
            self.id = result_edited.id
            self.session.close()
            
            return True
>>>>>>> Stashed changes



    def signout(self):
        print("signout successfully")
        self.id = None

    # def input_user_signup(self):
    #     self.username=input("please enter username : ")
    #     self.first_name = input("please enter first_name : ")
    #     self.last_name = input("please enter last_name : ")
    #     self.hash_password = input("please enter password : ")
        
    
    # def input_user_signin(self):
    #     self.username=input("please enter username : ")
    #     self.hash_password= input("please enter password : ")

    def get_id_user_login(self):
        return self.id

    def is_gmail(email):
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email))



def get_credentials_from_database(table_name):
    try:
        session = get_session()
        credentials = session.query(UserEntity).all()
        
        credentials_dict = {}
        for user in credentials:
            credentials_dict[user.username] = user.hash_password

        session.close()
        return credentials_dict

    except Exception as e:
        print("Error while fetching data from database:", e)
        return None


def get_credentials_from_database_gmail(table_name):
    try:
        session = get_session()
        credentials = session.query(UserEntity).all()
        
        credentials_dict = {}
        for user in credentials:
            credentials_dict[user.username] = user.gmail

        session.close()
        return credentials_dict

    except Exception as e:
        print("Error while fetching data from database:", e)
        return None

       
    
<<<<<<< Updated upstream
=======



def get_is_active(username_to_check):

    session = get_session()

    try:
        # Query the database to retrieve the is_active value
        user = session.query(UserEntity).filter_by(username=username_to_check).first()

        if user:
            is_active = user.is_active
            return is_active
        else:
            print(f"No user found with the username: {username_to_check}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the session
        session.close()


>>>>>>> Stashed changes
    