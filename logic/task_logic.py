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
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity,LeaderEntity,CommentEntity,UserTaskEntity,PriorityEnum,StatusEnum
import psycopg2

engine = create_engine("postgresql://postgres:postgres@localhost/trello")

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

        self.project_name_add_comment = None
        self.task_name_add_comment = None
        self.comment = None

        self.project_name_add_user = None
        self.task_name_add_user = None
        self.user_add_user = None
        self.user_id=self.user.get_id_user_login() 
        self.task_status = None
        self.task_priority = None
    def create_task(self):
        tempbool = self.input_task_info()

        if self.task_status not in StatusEnum or self.task_priority not in PriorityEnum:
            print("task_status or task_priority invalid")
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
                    db_model = TaskEntity(task_priority=self.task_priority,task_status=self.task_status,task_name=self.task_name,task_description=self.task_description,
                                          project_id=self.project_id,leader_id = self.leader_id)
                    self.session.add(db_model)
                    self.session.commit()
                    self.session.refresh(db_model)
                else:
                    print("this project has this task. ")

        


    def input_task_info(self):
        
        self.task_name = input("Enter task name: ")
        self.task_description = input("Enter task description: ")
        self.project_name = input("this task adds to which project?: ")
        self.task_status = input("please enter task_status")
        self.task_priority = input("please enter task_priority")
        return True
     
    def add_comment_to_task(self):
        self.user_id=self.user.get_id_user_login() 
        self.input_add_comment()
        project_name_exist=self.session.execute(select(
            ProjectEntity.project_name,
            ProjectEntity.id,
            UserProjectEntity.id,
            UserEntity.id,
            UserProjectEntity.user_id,
            UserProjectEntity.project_id
        ).join(
            UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        ).join(
            ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        ).where(
            ProjectEntity.project_name == self.project_name_add_comment,
            UserProjectEntity.user_id==self.user_id
        ))
        project_name_exist = project_name_exist.fetchone()
        if project_name_exist==None:
            print("you have not project with this name!")
        else:
            project_id = project_name_exist[1]
            task_exist = self.session.execute(select(TaskEntity).where(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_comment))
            task_exist = task_exist.scalars().one_or_none()
            if task_exist == None:
                print("this project dose not task with this task name!")
            else:
                comment = CommentEntity(comment_name=self.comment,project_id=project_id,user_id=self.user_id,task_id=task_exist.id)
                self.session.add(comment)
                self.session.commit()
                self.session.refresh(comment)
                
    def input_add_comment(self):
        self.project_name_add_comment = input("please enter project name")
        self.task_name_add_comment = input("please enter taskname")
        self.comment = input("please enter your comment")
        return True
    
    def add_user_to_task(self):
        self.input_add_user_task()
        project_name_exist=self.session.execute(select(
            ProjectEntity.project_name,
            ProjectEntity.id,
            UserProjectEntity.id,
            UserEntity.id,
            UserProjectEntity.user_id,
            UserProjectEntity.project_id
        ).join(
            UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        ).join(
            ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        ).where(
            ProjectEntity.project_name == self.project_name_add_user,
            UserProjectEntity.user_id==self.user_id
        ))
        project_name_exist = project_name_exist.fetchone()

        if project_name_exist==None:
            print("you have not project with this name!")
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_user))
            task=task.scalars().one_or_none()
            if task==None:
                print("this task dose not exist in this project")
            else:

                user_exsit = self.session.execute(select(UserEntity).filter_by(username = self.user_add_user))
                user_exsit = user_exsit.scalars().one_or_none()
                if user_exsit == None:
                    print("The user you want to add to your project does not exist")
                else:
                    user_in_task_exist = self.session.execute(select(UserTaskEntity).where(UserTaskEntity.task_id==task.id,UserTaskEntity.user_id==user_exsit.id))
                    user_in_task_exist = user_in_task_exist.scalars().one_or_none()
                    
                    if user_in_task_exist!= None:
                        print("The user has already been added to your task")
                    else:
                        user_exsit.tasks.append(task)
                        self.session.commit()
        



    def input_add_user_task(self):
        self.project_name_add_user = input("please enter project name")
        self.task_name_add_user = input("please enter project task name")
        self.user_add_user = input("please enter username for add")

    def list_users(self):
        self.project_name_list=input("please enter project name")
        self.task_name_list=input("please enter task name")
        user_in_task_exist=self.session.execute(select(
            ProjectEntity.project_name,
            TaskEntity.id,
            UserProjectEntity.id,
            UserEntity.id,
            UserProjectEntity.user_id,
            UserProjectEntity.project_id,
            TaskEntity.task_name,
            UserTaskEntity.id,
            UserEntity.id,
            UserTaskEntity.user_id,
            UserTaskEntity.task_id
        ).join(
            UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        ).join(
            ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        ).join(
            UserTaskEntity, UserEntity.id == UserTaskEntity.user_id
        ).join(
            TaskEntity, UserTaskEntity.task_id == TaskEntity.id
        ).where(
            ProjectEntity.project_name == self.project_name_list,
            TaskEntity.task_name == self.task_name_list,
            UserTaskEntity.user_id==self.user_id
        ))
        user_in_task_exist = user_in_task_exist.fetchone()
        if user_in_task_exist != None:
            task_id = user_in_task_exist[1]
            task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
            task = task.scalars().one_or_none()
            for user in task.users:
                print(user.username)
        else:
            print("dose not this task")

    def list_comment(self):
        self.project_name_list=input("please enter project name")
        self.task_name_list=input("please enter task name")
        user_in_task_exist=self.session.execute(select(
            ProjectEntity.project_name,
            TaskEntity.id,
            UserProjectEntity.id,
            UserEntity.id,
            UserProjectEntity.user_id,
            UserProjectEntity.project_id,
            TaskEntity.task_name,
            UserTaskEntity.id,
            UserEntity.id,
            UserTaskEntity.user_id,
            UserTaskEntity.task_id
        ).join(
            UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
        ).join(
            ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
        ).join(
            UserTaskEntity, UserEntity.id == UserTaskEntity.user_id
        ).join(
            TaskEntity, UserTaskEntity.task_id == TaskEntity.id
        ).where(
            ProjectEntity.project_name == self.project_name_list,
            TaskEntity.task_name == self.task_name_list,
            UserTaskEntity.user_id==self.user_id
        ))
        user_in_task_exist = user_in_task_exist.fetchone()
        if user_in_task_exist != None:
            task_id = user_in_task_exist[1]
            task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
            task = task.scalars().one_or_none()
            for comment in task.comments:
                print(comment.comment_name)

    def edit_task(self):
        self.user_id=self.user.get_id_user_login()
        project_name = input("enter project name: ")
        taskname_name = input("enter task name: ")
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
            ProjectEntity.project_name == project_name,
            UserProjectEntity.user_id==self.user_id
        ))
        
        project_name_exist = project_name_exist.fetchone()
        if project_name_exist==None:
                print("you dont have a project with this name")
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_user))
            task=task.scalars().one_or_none()
            if task==None:
                print("this task dose not exist in this project")
            else:
                user_in_task_exist = self.session.execute(select(UserTaskEntity).where(UserTaskEntity.task_id==task.id,UserTaskEntity.user_id==self.user_id))
                user_in_task_exist = user_in_task_exist.scalars().one_or_none()
                if user_in_task_exist ==None:
                    print("you not member in this project!")
                else:
                    task_description = input("please enter new description")
                    status = input("please enter new status")
                    priority = input("please enter new priority")
                    if task_description!="":
                        task.task_description = task_description
                    if status!="":
                        if status in StatusEnum:
                            task.status = status
                        else:
                            print("status invalid")
                    if priority!="":
                        if priority in PriorityEnum:
                            task.priority = priority
                        else:
                            print("invalid priority")
                    self.session.commit()

                    



