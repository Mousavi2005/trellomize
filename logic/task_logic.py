import argparse
from sqlalchemy import select, Column
from model.base_entity import TaskEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
from sqlalchemy.sql import text
from logic.user_logic import get_credentials_from_database
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import psycopg2

engine = create_engine("postgresql://postgres:foxit@localhost/user")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



class tasks:
    def __init__(self):
        self.session = get_session()
        self.task_name = None
        self.task_description = None

    def create_task(self):
        self.input_task_info()
        task = self.session.execute(select(TaskEntity).filter_by(task_name=self.task_name))
        result_edited = task.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("task is exist")
        else:
            db_model = TaskEntity(task_name=self.task_name,task_description=self.task_description)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)

    
    def input_task_info(self):
        self.task_name = input("Enter task name: ")
        self.task_description = input("Enter task description: ")



