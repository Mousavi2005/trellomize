import argparse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, text, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic
from logic.project_logic import project
from logic.manager_logic import manager
import psycopg2
from psycopg2 import sql
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from model.base_entity import UserEntity, ManagerEntity
import bcrypt
engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_admin(username: str, password: str) -> None:
    """This function adds Admin to database"""
    if not username or not password:
        print("Username and password are required to create an admin.")
        return
    x = manager()
    x.create_admin(username, password)

def purge_data():
    """This function clears all data in database"""
    console = Console()

    dbname = "t2"
    user = "postgres"
    password = "foxit"
    host = "localhost"
    port = "5432"  
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT tablename FROM pg_catalog.pg_tables
            WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
        """)

        tables = cur.fetchall()

        for table in tables:
            table_name = table[0]
            cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            text = Text(f"Dropped table {table_name}")
            console.print(text)

        text = Text("All tables droped successfully", style="bold green")
        console.print(text)



    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()

def main():
    """This function takes argumants in a terminal command .Based on command creates 'Admin' or deletes 'database'"""
    parser = argparse.ArgumentParser(description="Admin and database management tool")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    create_admin_parser = subparsers.add_parser("create-admin", help="Create an admin user")
    create_admin_parser.add_argument("--username", required=True, help="Admin username")
    create_admin_parser.add_argument("--password", required=True, help="Admin password")

    purge_data_parser = subparsers.add_parser("purge-data", help="Purge all data from the database")

    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.username, args.password)
    elif args.command == "purge-data":
        choice = Prompt.ask("[bold red]Are you sure? (y/n)[/bold red]")
        admin_name = Prompt.ask("Enter Admin username: ")
        admin_pass = Prompt.ask("Enter Admin password: ")
        if choice == 'y' or 'Y':
            session = get_session()
            admin = session.execute(select(ManagerEntity).where(ManagerEntity.admin_name == admin_name)).scalars().one_or_none()
            session.close()
            if admin is None or not bcrypt.checkpw(admin_pass.encode('utf-8'), admin.admin_pass.encode('utf-8')):
                print("invalid admin credentials")
            else:
                purge_data()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
