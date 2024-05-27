import argparse
from model.base_entity import UserEntity, ManagerEntity
from sqlalchemy import select, Column
from model.base_entity import ManagerEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
from sqlalchemy.sql import text
from logic.user_logic import get_credentials_from_database
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import psycopg2
from rich.console import Console
from rich.text import Text
from loguru import logger
import bcrypt

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


class manager:
    def __init__(self):
        self.session = get_session()


    def create_admin(self,admin_name: str,admin_pass: str) -> None:
        """This function adds Admin to database"""

        hashed_password = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # new_user = UserEntity(username=username, gmail=gmail, hash_password=hashed_password)

        console = Console()
        admin = self.session.execute(select(ManagerEntity).filter_by(admin_name=admin_name))
        result_edited = admin.scalars().one_or_none()

        # print(result_edited)
        if result_edited:
            logger.warning(f"Admin : {admin_name} , alreadt has account")

            text = Text("This Admin Already Has Account", style="bold red")
            console.print(text)
        else:
            logger.success(f"Admin : {admin_name} , created successfuly")

            db_model = ManagerEntity(admin_name=admin_name,admin_pass=hashed_password)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)
            text = Text("Admin Created", style="bold green")
            console.print(text)


def check_is_user_active(username: str) -> bool:
    """This function checks if a user is banned or not"""

    metadata = MetaData()
    metadata.reflect(bind=engine, only=['users'])
    Users = metadata.tables['users']
    session = get_session()
    
    try:
        result = session.query(Users.c.is_active).filter(Users.c.username == username).first()
        
        if result:

            return result.is_active
        else:
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        session.close()

# def ban_user(username: str) -> str:
#     """This function takes needed argumant and bans user"""
    
#     conn = psycopg2.connect(
#         dbname="t2",
#         user="postgres",
#         password="foxit",
#         host="localhost",
#         port="5432"  
#     )

#     cur = conn.cursor()

#     username_to_inactivate = username
#     isactive = 'f'
#     select_query = "SELECT COUNT(*) FROM users WHERE username = %s;"

#     cur.execute(select_query, (username,))
#     row_count = cur.fetchone()[0]
    
#     if row_count > 0 and check_is_user_active(username):
#         logger.success(f"user : {username} , banned successfuly")

#         update_query = "UPDATE users SET is_active = %s WHERE username = %s;"
#         cur.execute(update_query, (isactive,username))
#         conn.commit()
#         logger.success(f"user: {username} banned successfuly")
#         return "user banned successfully"

#     elif row_count == 0:
#         logger.warning(f"user: {username}, doesn't have account")

#         return "user does not exist. you may have entered username wrong."
#     else:
#         logger.warning(f"user: {username}, is already banned")

#         return "user is already baned"
        

#     cur.close()
#     conn.close()

def ban_user(username: str) -> str:
    """This function takes needed argumant and bans user"""
    try:
        engine = create_engine('postgresql://postgres:foxit@localhost:5432/t2')
        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(UserEntity).filter_by(username=username).first()

        if user:
            if user.is_active:
                user.is_active = False
                session.commit()
                session.close()
                logger.success(f"user : {username} , banned successfully")
                return "User banned successfully"
            else:
                session.close()
                logger.warning(f"user: {username}, is already banned")
                return "User is already banned"
        else:
            session.close()
            logger.warning(f"user: {username}, doesn't have account")
            return "User does not exist. You may have entered the username incorrectly."

    except Exception as e:
        logger.error(f"An error occurred while banning user {username}: {e}")
        return "An error occurred while banning the user"

def activate_user(username: str) -> str:
    """This function takes needed argumant and activates user"""


    conn = psycopg2.connect(
        dbname="t2",
        user="postgres",
        password="foxit",
        host="localhost",
        port="5432"  
    )

    cur = conn.cursor()

    username_to_activate = username
    isactive = 't'


    select_query = "SELECT COUNT(*) FROM users WHERE username = %s;"

    cur.execute(select_query, (username,))
    row_count = cur.fetchone()[0]
    
    if row_count > 0 and not check_is_user_active(username):
        logger.success(f"user: {username}, activated successfuly")

        update_query = "UPDATE users SET is_active = %s WHERE username = %s;"
        cur.execute(update_query, (isactive,username))
        conn.commit()

        return "user activated successfully"

    elif row_count == 0 :
        logger.warning(f"user: {username}, doesn't have account")

        return "user does not exist. you may have entered username wrong"
    else:
        logger.warning(f"user: {username}, is already active")

        return "user is already activated!"

    cur.close()
    conn.close()

def check_deleted_user(username: str) -> bool:
    """This function checks if a user is deleted or not"""

    metadata = MetaData()
    metadata.reflect(bind=engine, only=['users'])
    Users = metadata.tables['users']
    
    session = get_session()
    
    try:
        result = session.query(Users.c.is_deleted).filter(Users.c.username == username).first()
        
        if result:
            logger.success(f"user : {username}, is deleted")

            return result.is_deleted
        else:
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        session.close()

def delet_user(username: str) -> str:
    """This function takes needed argumant and deletes user"""

    conn = psycopg2.connect(
        dbname="t2",
        user="postgres",
        password="foxit",
        host="localhost",
        port="5432"  
    )

    cur = conn.cursor()

    username_to_activate = username
    isdeleted = 't'


    select_query = "SELECT COUNT(*) FROM users WHERE username = %s;"

    cur.execute(select_query, (username,))
    row_count = cur.fetchone()[0]
    
    if row_count > 0 and  not check_deleted_user(username):
        logger.success(f"user: {username}, deleted successfuly")

        update_query = "UPDATE users SET is_deleted = %s WHERE username = %s;"
        cur.execute(update_query, (isdeleted,username))
        conn.commit()

        return "user deleted successfully"

    elif row_count == 0 :
        logger.warning(f"user: {username}, doesn't have account!")

        return "user does not exist. you may have entered username wrong"
    else:
        logger.warning(f"user: {username}, is already deleted!")
        
        return "user is already deleted!"

    cur.close()
    conn.close()

