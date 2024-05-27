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
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity,LeaderEntity, CommentEntity, UserTaskEntity,StatusEnum,PriorityEnum
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
      


    def create_task(self, add_task_to_which_project, task_name, task_description,task_status,task_priority):
        self.user_id = self.user.get_id_user_login() 
        self.project_name = add_task_to_which_project
        if task_status not in StatusEnum or task_priority not in PriorityEnum:
            print("task_status or task_priority invalid")
        else:
            project_name_exist = self.session.execute(select(
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
                UserProjectEntity.user_id == self.user_id
            ))
            
            project_name_exist = project_name_exist.fetchone()
            if project_name_exist == None:
                    return self.user_id
            else:
                
                self.project_id = project_name_exist[1]


        

                # tempbool = self.input_task_info()
                self.task_name = task_name
                self.task_description = task_description
                self.task_status=task_status
                self.task_priority=task_priority
                
                if True:
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
                    # print(exist_task)
                    if exist_task == None or exist_task == []:
                        db_model = TaskEntity(task_status=self.task_status,task_priority=self.task_priority,task_name=self.task_name,task_description=self.task_description,
                                            project_id=self.project_id,leader_id = self.leader_id)
                        self.session.add(db_model)
                        self.session.commit()
                        self.session.refresh(db_model)
                        return "Task Made Successfully"
                    else:
                        return "this project has this task"




    def add_comment_to_task(self, project_name_add_comment, task_name_add_comment, comment):

        self.user_id=self.user.get_id_user_login()

        self.project_name_add_comment = project_name_add_comment
        self.task_name_add_comment = task_name_add_comment
        self.comment = comment

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
            return "you are not in a project with this name!"

        else:
            project_id = project_name_exist[1]
            task_exist = self.session.execute(select(TaskEntity).where(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_comment))
            task_exist = task_exist.scalars().one_or_none()
            if task_exist == None:
                # print("this project dose not task with this task name!")
                return "this project dose not have task with this task name!"
            else:
                comment = CommentEntity(comment_name=self.comment,project_id=project_id,user_id=self.user_id,task_id=task_exist.id)
                self.session.add(comment)
                self.session.commit()
                self.session.refresh(comment)
                return "Comment Added succesfully"


    

    def add_user_to_task(self, pname, tname, uname):
        self.user_id=self.user.get_id_user_login()

        self.project_name_add_user = pname
        self.task_name_add_user = tname
        self.user_add_user = uname
        # self.input_add_user_task()

        project_name_exist = self.session.execute(select(
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
            UserProjectEntity.user_id == self.user_id
        ))
        project_name_exist = project_name_exist.fetchone()


        if project_name_exist==None:
            # print("you have not project with this name!")
            return "you dont have project with this name!"
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_user))
            task=task.scalars().one_or_none()
            if task==None:
                # print("this task dose not exist in this project")
                return "This Project Doesn't Have This Task"
            else:
                user_exsit = self.session.execute(select(UserEntity).filter_by(username = self.user_add_user))
                user_exsit = user_exsit.scalars().one_or_none()
                user_exist_id=user_exsit.id
                user_exsit = self.session.execute(select(
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
                UserProjectEntity.user_id == user_exist_id
            ))
                user_exsit = user_exsit.fetchone()
                
                if user_exsit == None or user_exsit==[]:
                    # print("The user you want to add to your project does not exist")
                    # return "The user you want to add to your project does not exist"
                    return "This user dosnt have account or dise not this project"
                else:
                    user_exsit = self.session.execute(select(UserEntity).filter_by(id = user_exist_id))
                    user_exsit = user_exsit.scalars().one_or_none()
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
                        ProjectEntity.project_name == self.project_name_add_user,
                        TaskEntity.task_name == self.task_name_add_user,
                        UserTaskEntity.user_id==user_exsit.id
                    ))
                    user_in_task_exist = user_in_task_exist.fetchone()

                    if user_in_task_exist!= None:
                        # print("The user has already been added to your task")
                        return "This user has already been added to your task"
                    else:
                        user_exsit.tasks.append(task)
                        self.session.commit()
                        return "Successful"
                

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