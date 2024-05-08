import argparse
from tabulate import tabulate
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import user, get_credentials_from_database
from logic.project_logic import project
from logic.manager_logic import manager

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

engine = create_engine("postgresql://postgres:foxit@localhost/trello")
Base.metadata.create_all(engine)

console = Console()

console.print("[bold cyan]Welcome to TRELLOMIZE[/bold cyan]")

choice = 0
while True:
    console.print("1. Create new Project ")
    console.print("2. Add user to project ")
    console.print("3. Add task to project ")
    console.print("4. Exit ")
    choice = input("Enter your choice: ")

    if choice == '1' :
        project1 = project()
        # print("Project made successfully ")

    elif choice == '2' :
        username = Prompt.ask("[bold cyan]Enter your username: [/bold cyan]")
        users = get_credentials_from_database('users')
        if username not in users.keys():
            print("This user doesn't have account on trellomoize")
        else:
            print("User added to project")
        # have to add this user name to project
        # project creator cannot add himself to project





# table_name = "users"


# choice = 0
# while True:
#     console.print("1. Sign up ")
#     console.print("2. Login ")
#     console.print("3. Exit ")
#     choice = input("Enter your choice: ")
#     if choice == '1' :
#         break
#     elif choice == '2' :
#         break
#     elif choice == '3' :
#         console.print("[bold red]Good Bye[/bold red]")
#         break
#     else:
#         console.print("[bold red]Please choose between options.[/bold red] ")

# if choice == '1' :
#     user = user()

# elif choice == '2':
#     while True:
#         username = Prompt.ask("[bold cyan]Enter your username: [/bold cyan]")
#         password = Prompt.ask("[bold cyan]Enter your password: [/bold cyan]", password=True)
#         credentials = get_credentials_from_database(table_name)
#         for key, value in credentials.items():
#             if key == username and value == password:
#                 print("you entered succesfuly")
#             else:
#                 print("you entered username or password wrong \nTry again")
        





# x = manager()











        #   UPDATING DATABASE CODE
# import psycopg2

# # Connect to the database
# conn = psycopg2.connect(
#     dbname="trello",
#     user="postgres",
#     password="foxit",
#     host="localhost",  # Assuming your local PostgreSQL is running on localhost
#     port="5432"  # Default PostgreSQL port
# )
# cursor = conn.cursor()

# # Drop all tables
# drop_tables_query = """
#     DROP SCHEMA public CASCADE;
#     CREATE SCHEMA public;
# """
# cursor.execute(drop_tables_query)

# # Commit the transaction
# conn.commit()

# # Close the connection
# conn.close()
