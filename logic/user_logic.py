# from ..main import get_session
from sqlalchemy import select, text, update, MetaData, Table
from model.base_entity import UserEntity, ManagerEntity, LeaderEntity, ProjectEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import regex as re
from loguru import logger
import bcrypt
from typing import Union
import copy

engine = create_engine("postgresql://postgres:foxit@localhost/t2")
logger.add(
    "file1",
    format="{time} {level} {message}",
    rotation="1 MB"
)

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

    # def signup_user(self, username: str, gmail: str, password: str) -> bool:
    #     """This function takes needed arguments and adds user to the database"""
        
    #     existing_user = self.session.query(UserEntity).filter(UserEntity.username == username).first()
    #     # user = self.session.execute(select(UserEntity).where(UserEntity.username == username)).scalars().one_or_none()

    #     if existing_user:
    #         logger.warning(f"Username '{username}' is already taken.")

    #         return False

    #     existing_email = self.session.query(UserEntity).filter(UserEntity.gmail == gmail).first()
    #     if existing_email:
    #         logger.warning(f"Email '{gmail}' is already registered.")

    #         return False

    #     if not self.is_gmail(gmail):
    #         logger.warning(f"Email '{gmail}' is not valid.")

    #         return False

    #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    #     new_user = UserEntity(username=username, gmail=gmail, hash_password=hashed_password)

    #     try:
    #         logger.success(f"{username} user signed up successfully")

    #         self.session.add(new_user)
    #         self.session.commit()
    #         existing_user = self.session.query(UserEntity).filter(UserEntity.username == username).first()
    #         self.id = existing_user.id

    #         return True
    #     except Exception as e:
    #         logger.error(f"Error occurred while signing up {username} user: {e}")

    #         self.session.rollback()
    #         return False
    #     finally:
    #         self.session.close()

    def signup_user(self, username: str, gmail: str, password: str) -> bool:
        """This function takes needed arguments and adds user to the database"""
        try:
            existing_user = self.session.query(UserEntity).filter(UserEntity.username == username).first()
            
            if existing_user:
                logger.warning(f"Username '{username}' is already taken.")
                return False

            existing_email = self.session.query(UserEntity).filter(UserEntity.gmail == gmail).first()
            if existing_email:
                logger.warning(f"Email '{gmail}' is already registered.")
                return "UG"

            if not self.is_gmail(gmail):
                logger.warning(f"Email '{gmail}' is not valid.")
                return "NVG"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = UserEntity(username=username, gmail=gmail, hash_password=hashed_password)

            logger.success(f"{username} user signed up successfully")

            self.session.add(new_user)
            self.session.commit()
            existing_user = self.session.query(UserEntity).filter(UserEntity.username == username).first()
            self.id = existing_user.id

            return True
        except Exception as e:
            logger.error(f"Error occurred while signing up {username} user: {e}")
            self.session.rollback()
            return False
        finally:
            self.session.close()

    # def login_user(self, username: str, password: str) -> Union[bool, str]:
        """This function takes needed arguments and connects user to the database (if user doesn't have account they have to signup first)"""

        session = get_session()
        admin = session.execute(select(ManagerEntity).where(ManagerEntity.admin_name == username)).scalars().one_or_none()
        
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin.admin_pass.encode('utf-8')):
            logger.success(f"{username} username logged in as Admin successfully")

            return "Admin"

        temp_active = get_is_active(username)
        user = self.session.execute(select(UserEntity).where(UserEntity.username == username)).scalars().one_or_none()

        if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.hash_password.encode('utf-8')):
            logger.warning(f"username : {username} and password: {password} do not match!")

            return False

        if not temp_active:
            logger.warning(f"{username} username is banned")

            return "NA"

        logger.success(f"{username} user logged in successfully")

        self.id = user.id
        self.session.close()
        return True

    def login_user(self, username: str, password: str) -> Union[bool, str]:
        """This function takes needed arguments and connects user to the database (if user doesn't have account they have to signup first)"""
        try:
            session = get_session()
            admin = session.execute(select(ManagerEntity).where(ManagerEntity.admin_name == username)).scalars().one_or_none()
            
            if admin and bcrypt.checkpw(password.encode('utf-8'), admin.admin_pass.encode('utf-8')):
                logger.success(f"{username} username logged in as Admin successfully")
                return "Admin"

            temp_active = get_is_active(username)
            user = self.session.execute(select(UserEntity).where(UserEntity.username == username)).scalars().one_or_none()

            if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.hash_password.encode('utf-8')):
                logger.warning(f"username : {username} and password: {password} do not match!")
                return False

            if not temp_active:
                logger.warning(f"{username} username is banned")
                return "NA"

            logger.success(f"{username} user logged in successfully")
            self.id = user.id
            return True
        except Exception as e:
            logger.error(f"An error occurred while logging in {username} user: {e}")
            return False
        finally:
            self.session.close()

    # def list_projects(self):
        """This function shows a list of projects that user is in them (added to them)"""

        result = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = result.scalars().one_or_none()

        if user is None:
            logger.warning("User isn't in any project")

            return False

        if not hasattr(user, 'projects') or len(user.projects) == 0:
            logger.warning("User isn't in any project")

            return False

        logger.success("User saw projects he's added to")

        projects_data = [
            {
                project.project_name,
            }
            for project in user.projects
        ]

        return projects_data

    def list_projects(self):
        """This function shows a list of projects that user is in them (added to them)"""
        try:
            result = self.session.execute(select(UserEntity).filter_by(id=self.id))
            user = result.scalars().one_or_none()

            if user is None:
                logger.warning("User isn't in any project")
                return False

            if not hasattr(user, 'projects') or len(user.projects) == 0:
                logger.warning("User isn't in any project")
                return False

            logger.success("User saw projects he's added to")

            projects_data = [
                {
                    project.project_name,
                }
                for project in user.projects
            ]

            return projects_data
        except Exception as e:
            logger.error(f"An error occurred while listing projects for user {self.id}: {e}")
            return False
        finally:
            self.session.close()

    # def list_tasks(self):
        """This function shows a list of tasks that user is in them (added to them)"""

        result = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = result.scalars().one_or_none()

        if user is None:
            logger.warning("User isn't in any task")

            return False

        if not hasattr(user, 'tasks') or len(user.tasks) == 0:
            logger.warning("User isn't in any task")

            return False

        logger.success("User saw tasks he's added to")

        tasks_data = [
            {
                task.task_name,
            }
            for task in user.tasks
        ]

        return tasks_data

    def list_tasks(self):
        """This function shows a list of tasks that user is in them (added to them)"""
        try:
            result = self.session.execute(select(UserEntity).filter_by(id=self.id))
            user = result.scalars().one_or_none()

            if user is None:
                logger.warning("User isn't in any task")
                return False

            if not hasattr(user, 'tasks') or len(user.tasks) == 0:
                logger.warning("User isn't in any task")
                return False

            logger.success("User saw tasks he's added to")

            tasks_data = [
                {
                    task.task_name,
                }
                for task in user.tasks
            ]

            return tasks_data
        except Exception as e:
            logger.error(f"An error occurred while listing tasks for user {self.id}: {e}")
            return False
        finally:
            self.session.close()

    def list_leader_project(self):
        # self.user_id = self.use.get_id_user_login()

        user = self.session.execute(select(UserEntity).filter_by(id=self.id))
        user = user.scalars().one_or_none()
        user_id = user.id
        projects_id = self.session.execute(select(LeaderEntity.project_id).filter_by(user_id=user_id)).scalars().all()
        projects = self.session.execute(select(ProjectEntity).where(ProjectEntity.id.in_(projects_id))).scalars().all()

        tasks_data = [
            {
                p.project_name,
            }
                for p in projects
        ]

        return tasks_data
        # for project in projects:
        #     print(project.project_name)


    def get_id_user_login(self):
        """This function returns user id after login"""

        return self.id

    def is_gmail(self,email: str) -> bool:
        """This functions checks if a gmail is valid or not"""
        
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email))



def get_credentials_from_database(table_name):
    """This function connects to database and returns username and password of users in a dictionary"""
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
    """This function connects to database and returns username and gmail of users in a dictionary"""

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
    """This function connects to database and returns username and user id of users in a dictionary"""

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
    """This function connects to database and checks if a user is banned or not"""


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
















    # def signup_user(self, username, gmail, password):
        """This function takes needed arguments and adds user to database"""
        # Check if the username already exists
        # existing_user = self.session.query(UserEntity).filter(UserEntity.username == username).first()
        # if existing_user:
        #     logger.warning(f"Username '{username}' is already taken.")
        #     return False

        # # Check if the email already exists
        # existing_email = self.session.query(UserEntity).filter(UserEntity.gmail == gmail).first()
        # if existing_email:
        #     logger.warning(f"Email '{gmail}' is already registered.")
        #     return False

        # # Check if the email is valid
        # if not self.is_gmail(gmail):
        #     logger.warning(f"Email '{gmail}' is not valid.")
        #     return False

        # # Hash the password
        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # # Create a new user entity
        # new_user = UserEntity(username=username, gmail=gmail, hash_password=hashed_password)
        
        # # Add the new user to the session and commit changes
        # try:
        #     self.session.add(new_user)
        #     self.session.commit()
        #     logger.success(f"{username} user signed up successfully")
        #     return True
        # except Exception as e:
        #     logger.error(f"Error occurred while signing up {username} user: {e}")
        #     self.session.rollback()
        #     return False
        # finally:
            # self.session.close()

    