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
from logic.project_logic import project, get_user_credentials
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity
import psycopg2

engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



class tasks:
    def __init__(self,project=None,user=None):
        self.user = user
        self.proj = project
        self.session = get_session()
        self.task_name = None
        self.task_description = None
        self.project_id = None
        self.session = get_session()

    def create_task(self):
        project_name = input("Enter project name/: ")
        username = input("Enter  username/: ")

    # ;;;
        tempproject = self.session.query(ProjectEntity).filter_by(project_name=project_name).all()
        print(tempproject)
        specific_user_id = 123

        # Query to find the project ID associated with the specific user ID
        user_project = self.session.query(ProjectEntity).filter_by(username=username).first()

        if user_project:
            self.project_id = user_project.id
        #     print(f"Project ID for user ID {specific_user_id} is: {project_id}")
        # else:
        #     print(f"No project found for user ID {specific_user_id}")


        if self.project_id != None:
            # check if this project has this task or not

            tempbool = self.input_task_info()
            # print(tempbool)
            if tempbool == True:
                # print("qqqqqqqqqqqqqqqqqqqqqqqq")
                task = self.session.execute(select(TaskEntity).filter(TaskEntity.task_name==self.task_name, TaskEntity.project_id == self.project_id))
                task = task.scalars().one_or_none()
                if task == None:
                    # print("--------------------wewe-----------------")
                    db_model = TaskEntity(task_name=self.task_name,task_description=self.task_description,project_id=self.project_id)
                    self.session.add(db_model)
                    self.session.commit()
                    self.session.refresh(db_model)
            else:
                print("this project has this task. ")

        #     task_name_exist = self.session.execute(select(
        #     ProjectEntity.project_name,
        #     UserProjectEntity.id,
        #     UserEntity.id,
        # ).join(
        #     UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        # ).join(
        #     ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        # ).where(
        #     ProjectEntity.project_name == self.project_name,
            
        # ))
            # project_name_exist = project_name_exist.scalars().all()
            # if project_name_exist != []:
            #     print("this project_name is exist")
            #     return False
            # model_project = ProjectEntity(project_name=self.project_name, username=user.username, hash_password=user.hash_password, first_name=user.first_name, last_name=user.last_name)
            # user.projects.append(model_project)
            # model_project.users.append(user)
            # self.session.add(model_project)
            # self.session.commit()
            # self.session.refresh(model_project)
                # print("create task successfull")
        else:
            print("not authentication. you should login or signup")


    def input_task_info(self):
        pname = input("enter project name: ")
        username = input("Enter user-name: ")
        task_name = input("Enter task name: ")
        task_description = input("Enter task description: ")
        x = get_user_credentials()
        # dic = get_credentials_from_database2("tasks")
        user_project = self.session.query(ProjectEntity).filter_by(username=self.user.username).first()
        # print(x)
        # print(dic)
        # print(x)


        t = 0
        for key , value in x.items():
            print(key)
            print(value)
            if key == pname and value == username:
                # print("========================================")
                t = 1
        if t == 0 :
            return False

        
                
        if t == 1:
            task = get_credentials_from_database2("tasks")
            # print(dic)
            # print("----------------r-rr--------------r")
            # user_project = self.session.query(ProjectEntity).filter_by(username=self.user.username).first()
            for taskname, projectid in task.items():
                if taskname == task_name and projectid == user_project.id:
                    # if projectid == user_project.id:
                    print("--------------------5------------------")
                    return False
                        
            self.task_name = task_name
            self.task_description = task_description
            return True


def get_credentials_from_database2(table_name):
    try:
        session = get_session()
        credentials = session.query(TaskEntity).all()
        credentials_dict = {credential.task_name: credential.project_id for credential in credentials}
        session.close()
        return credentials_dict
    except Exception as e:
        print("Error while fetching data from database:", e)