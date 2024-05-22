# from ..main import get_session
from sqlalchemy import select, text, update, MetaData, Table
from model.base_entity import UserEntity, ManagerEntity
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
        self.gmail = None
        self.hash_password = None
        self.first_name = None
        self.last_name = None
        self.id = None
        self.session = get_session()


    def signup_user(self,username, gmail, password):
        temdictionary = get_credentials_from_database('users')
        k = 0
        for key, value in temdictionary.items():
            if key == username:
                k = 1

        # session = SessionLocal()
        is_valid_gmail = self.is_gmail(gmail)
        if k == 0 and is_valid_gmail:
            new_user = UserEntity(username=username, gmail=gmail , hash_password=password)
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
        else : 
            return False



    def login_user(self,username, password):

        session = get_session()
        admin = session.execute(select(ManagerEntity).where(ManagerEntity.admin_name == username, ManagerEntity.admin_pass == password))
        result_edited = admin.scalars().one_or_none()
        if result_edited != None :
            return "Admin"

        # session = SessionLocal()
        temp_active = get_is_active(username)
        user = self.session.execute(select(UserEntity).where(UserEntity.username == username, UserEntity.hash_password == password))
        result_edited = user.scalars().one_or_none()
        if result_edited == None or not temp_active:
            return False
        else:
            # result_edited = user.scalars().one_or_none()
            self.id = result_edited.id
            self.session.close()
            
            return True


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

    def is_gmail(self, email):
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

       
    



def get_is_active(username_to_check):
    # Define the SQLAlchemy engine and session
    # engine = create_engine('postgresql://your_username:your_password@localhost/your_database')
    # Session = sessionmaker(bind=engine)
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

# # Example usage:
# username_to_check = "desired_username"
# is_active_value = get_is_active(username_to_check)
# if is_active_value is not None:
#     print(f"The is_active value for user {username_to_check} is: {is_active_value}")
    