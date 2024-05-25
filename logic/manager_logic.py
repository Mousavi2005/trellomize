import argparse
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
        console = Console()
        admin = self.session.execute(select(ManagerEntity).filter_by(admin_name=admin_name))
        result_edited = admin.scalars().one_or_none()
        # print(result_edited)
        if result_edited:
            text = Text("This Admin Already Has Account", style="bold red")
            console.print(text)

        else:
            db_model = ManagerEntity(admin_name=admin_name,admin_pass=admin_pass)
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

def ban_user(username: str) -> str:
    """This function takes needed argumant and bans user"""
    logger.debug(f"attempting to ban user: {username}")
    

    conn = psycopg2.connect(
        dbname="t2",
        user="postgres",
        password="foxit",
        host="localhost",
        port="5432"  
    )

    cur = conn.cursor()

    username_to_inactivate = username
    isactive = 'f'


    select_query = "SELECT COUNT(*) FROM users WHERE username = %s;"

    cur.execute(select_query, (username,))
    row_count = cur.fetchone()[0]
    
    if row_count > 0 and check_is_user_active(username):
        update_query = "UPDATE users SET is_active = %s WHERE username = %s;"
        cur.execute(update_query, (isactive,username))
        conn.commit()
        logger.success(f"user: {username} banned successfuly")
        return "user banned successfully"

    elif row_count == 0:
        logger.warning(f"user: {username} doesn't have account")

        return "user does not exist. you may have entered username wrong."
    else:
        logger.warning(f"user: {username} is already banned")

        return "user is already baned"
        

    cur.close()
    conn.close()

def activate_user(username: str) -> str:
    """This function takes needed argumant and activates user"""
    logger.debug("Atemting to activate a user")


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
        logger.success(f"user: {username} activates successfuly")

        update_query = "UPDATE users SET is_active = %s WHERE username = %s;"
        cur.execute(update_query, (isactive,username))
        conn.commit()

        return "user activated successfully"

    elif row_count == 0 :
        logger.warning(f"user: {username} doesn't have account")

        return "user does not exist. you may have entered username wrong"
    else:
        logger.warning(f"user: {username} is already active")

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
    logger.debug("Atempting to delete a user")


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
        logger.success(f"user: {username} deleted successfuly")

        update_query = "UPDATE users SET is_deleted = %s WHERE username = %s;"
        cur.execute(update_query, (isdeleted,username))
        conn.commit()

        return "user deleted successfully"

    elif row_count == 0 :
        logger.warning(f"user: {username} doesn't have account!")

        return "user does not exist. you may have entered username wrong"
    else:
        logger.warning(f"user: {username} is already deleted!")
        
        return "user is already deleted!"

    cur.close()
    conn.close()

