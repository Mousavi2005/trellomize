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

engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class manager:
    def __init__(self):
        self.session = get_session()
        # self.create_admin_from_input()


    def create_admin(self,admin_name,admin_pass):
        admin = self.session.execute(select(ManagerEntity).filter_by(admin_name=admin_name))
        result_edited = admin.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("admin is exist")
        else:
            db_model = ManagerEntity(admin_name=admin_name,admin_pass=admin_pass)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)

def check_banned_user(username):
    session = get_session()  # Assuming get_session() function returns a SQLAlchemy session

    try:
        # Execute a raw SQL query to fetch the password for the given username
        query = text("SELECT is_active FROM users WHERE username = :username")
        
        result = session.execute(query, {"username": username}).fetchone()

        if result:
            situation = result[0]
            return situation
        else:
            print(f"User with username '{username}' does not exist.")

    except Exception as e:
        print("Error while fetching data from database:", e)

    finally:
        session.close()


def ban_user():
    console = Console()

    username = input("Enter username: ")
    conn = psycopg2.connect(
        dbname="trello",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"  
    )

    cur = conn.cursor()

    username_to_inactivate = username
    isactive = 'f'


    select_query = "SELECT COUNT(*) FROM users WHERE username = %s;"

    cur.execute(select_query, (username,))
    row_count = cur.fetchone()[0]
    
    if row_count > 0 and check_banned_user(username):
        decision = Prompt.ask('[bold red]Are you sure? (yes/no)  : [/bold red]')
        if decision == 'yes' :
            update_query = "UPDATE users SET is_active = %s WHERE username = %s;"
            cur.execute(update_query, (isactive,username))
            conn.commit()
            console.print("[bold green]user banned successfully.[/bold green]")
        else :
            pass
    else:
        console.print("[bold red]user does not exist. you may have entered username wrong.[/bold red]")

    cur.close()
    conn.close()



