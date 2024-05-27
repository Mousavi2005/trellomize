# from ..main import get_session
from sqlalchemy import select, text, update, MetaData, Table
from model.base_entity import UserEntity, ManagerEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import regex as re


engine = create_engine("postgresql://postgres:postgres@localhost/trello")

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


    def signup_user(self,username, gmail, password):
        temdictionary = get_credentials_from_database('users')
        k = 0
        for key, value in temdictionary.items():
            if key == username:
                k = 1

        gmail_dictionary = get_credentials_from_database_gmail('users')
        t = 0
        for key, value in gmail_dictionary.items():
            if value == gmail:
                t = 1
        

        is_valid_gmail = self.is_gmail(gmail)
        if k == 0 and is_valid_gmail and t == 0:
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
        elif not is_valid_gmail:
            return "NVG"
        
        elif t == 1 :
            return "UG"

        else : 
            return False


    def login_user(self,username, password):

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
    def list_tasks(self):
        user = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = user.scalars().one_or_none()
        if len(user.tasks)==0:
            print("dose not exist any task")
        else:
            for task in user.tasks:
                print(task.task_name)

    def list_projects(self):
        user = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = user.scalars().one_or_none()
        if len(user.projects)==0:
            print("dose not exist any project")

    def list_leader_project(self):

        user = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = user.scalars().one_or_none()
        user_id = user.id
        projects_id = self.session.execute(select(LeaderEntity.project_id).filter_by(user_id=user_id)).scalars().all()
        projects = self.session.execute(select(ProjectEntity).where(ProjectEntity.id.in_(projects_id))).scalars().all()
        for project in projects:
            print(project.project_name)
            
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
        # print("---")
        return self.id
        # print(self.id)

    def is_gmail(self,email):
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


def get_credentials_from_database_user_id():
    try:
        session = get_session()
        credentials = session.query(UserEntity).all()
        
        credentials_dict = {}
        for user in credentials:
            credentials_dict[user.username] = user.id
        session.close()
        return credentials_dict

    except Exception as e:
        print("Error while fetching data from database:", e)
        return None

       
    



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


    