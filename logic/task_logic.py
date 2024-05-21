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
# from logic.project_logic import project, get_user_credentials
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity,LeaderEntity
import psycopg2

engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



class Tasks:
    def __init__(self,project=None,user=None):
        self.user = user
        self.proj = project
        self.session = get_session()

        self.task_name = None
        self.task_description = None

        self.project_name = None
        self.project_id = None
        self.user_id = None
        self.leader_id = None

    def create_task(self):
        self.project_name = input("this task adds to which project?: ")
        self.user_id=self.user.get_id_user_login() 
        project_name_exist=self.session.execute(select(
            ProjectEntity.project_name,
            ProjectEntity.id.label("project_id"),
            UserProjectEntity.id,
            UserEntity.id,
            UserProjectEntity.user_id,
            UserProjectEntity.project_id
        ).join(
            UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        ).join(
            ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        ).where(
            ProjectEntity.project_name == self.project_name,
            UserProjectEntity.user_id==self.user_id
        ))
        
        project_name_exist = project_name_exist.fetchone()
        if project_name_exist==None:
                print("you dont have a project with this name")
        else:
            
            self.project_id = project_name_exist[1]


       

            tempbool = self.input_task_info()
            if tempbool == True:
                leader = self.session.execute(select(LeaderEntity).filter(LeaderEntity.project_id==self.project_id,LeaderEntity.user_id==self.user_id))
                leader = leader.scalars().one_or_none()
                self.leader_id =leader.id
                

                exist_task = self.session.execute(
                    select(TaskEntity).where(
                        TaskEntity.project_id == self.project_id,
                        TaskEntity.task_name == self.task_name
                    )
                )
                exist_task = exist_task.scalars().one_or_none()
                print(exist_task)
                if exist_task == None or exist_task == []:
                    db_model = TaskEntity(task_name=self.task_name,task_description=self.task_description,
                                          project_id=self.project_id,user_id=self.user_id,leader_id = self.leader_id)
                    self.session.add(db_model)
                    self.session.commit()
                    self.session.refresh(db_model)
            else:
                print("this project has this task. ")

        


    def input_task_info(self):
        
        self.task_name = input("Enter task name: ")
        self.task_description = input("Enter task description: ")
        return True
        # x = get_user_credentials()
        # dic = get_credentials_from_database2("tasks")
        # user_project = self.session.execute(select(ProjectEntity).filter_by(username=self.user_id))
        # print(x)
        # print(dic)
        # print(x)


        # t = 0
        # for key , value in x.items():
        #     print(key)
        #     print(value)
        #     if key == pname and value == username:
        #         # print("========================================")
        #         t = 1
        # if t == 0 :
        #     return False

        
                
        # if t == 1:
        #     task = get_credentials_from_database2("tasks")
        #     # print(dic)
        #     # print("----------------r-rr--------------r")
        #     # user_project = self.session.query(ProjectEntity).filter_by(username=self.user.username).first()
        #     for taskname, projectid in task.items():
        #         if taskname == task_name and projectid == user_project.id:
        #             # if projectid == user_project.id:
        #             print("--------------------5------------------")
        #             return False
                        
        #     self.task_name = task_name
        #     self.task_description = task_description
        #     return True


# def get_credentials_from_database2(table_name):
#     try:
#         session = get_session()
#         credentials = session.query(TaskEntity).all()
#         credentials_dict = {credential.task_name: credential.project_id for credential in credentials}
#         session.close()
#         return credentials_dict
#     except Exception as e:
#         print("Error while fetching data from database:", e)