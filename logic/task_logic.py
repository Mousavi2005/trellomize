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
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity,LeaderEntity, CommentEntity, UserTaskEntity
import psycopg2
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
        # self.user_id = self.user.get_id_user_login() 

    # def list_users(self, pname, tname):
    #     """This function returns list of users in task (if task exisst)"""
    #     self.user_id = self.user.get_id_user_login()

    #     self.project_name_list= pname
    #     self.task_name_list = tname

    #     user_in_task_exist=self.session.execute(select(
    #         ProjectEntity.project_name,
    #         TaskEntity.id,
    #         UserProjectEntity.id,
    #         UserEntity.id,
    #         UserProjectEntity.user_id,
    #         UserProjectEntity.project_id,
    #         TaskEntity.task_name,
    #         UserTaskEntity.id,
    #         UserEntity.id,
    #         UserTaskEntity.user_id,
    #         UserTaskEntity.task_id
    #     ).join(
    #         UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
    #     ).join(
    #         ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
    #     ).join(
    #         UserTaskEntity, UserEntity.id == UserTaskEntity.user_id
    #     ).join(
    #         TaskEntity, UserTaskEntity.task_id == TaskEntity.id
    #     ).where(
    #         ProjectEntity.project_name == self.project_name_list,
    #         TaskEntity.task_name == self.task_name_list,
    #         UserTaskEntity.user_id==self.user_id
    #     ))
    #     user_in_task_exist = user_in_task_exist.fetchone()
    #     if user_in_task_exist != None:
    #         logger.success("successfuly showed users of a task list")

    #         task_id = user_in_task_exist[1]
    #         task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
    #         task = task.scalars().one_or_none()

    #         projects_data = [
    #         {
    #             user.username,
    #         }
    #         for user in task.users
    #         ]

    #         return projects_data

    #     else:
    #         logger.warning(f"{tname} task doesn't have any users")
    #         # print("dose not this task")
    #         print("This task doesn't have user")
    #         return False

    def list_users(self, pname, tname):
        """This function returns list of users in task (if task exists)"""
        try:
            self.user_id = self.user.get_id_user_login()

            self.project_name_list = pname
            self.task_name_list = tname

            user_in_task_exist = self.session.execute(
                select(
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
                    UserTaskEntity.user_id == self.user_id
                )
            )
            user_in_task_exist = user_in_task_exist.fetchone()

            if user_in_task_exist is not None:
                # logger.success("Successfully showed users of a task list")

                task_id = user_in_task_exist[1]
                task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
                task = task.scalars().one_or_none()

                if task is None:
                    logger.error(f"Task with id {task_id} not found")
                    return "Task not found"

                logger.success("Successfully showed users of a task list")

                projects_data = [
                    {
                        "username": user.username,
                    }
                    for user in task.users
                ]

                return projects_data
            else:
                logger.warning(f"{tname} task doesn't have any users")
                # print("This task doesn't have users")
                return False
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    # def list_comment(self, pname, tname):
    #     """This function shows list of comments in a task (if task exists)"""

    #     self.user_id = self.user.get_id_user_login()
    #     self.project_name_list = pname
    #     self.task_name_list = tname

    #     user_in_task_exist=self.session.execute(select(
    #         ProjectEntity.project_name,
    #         TaskEntity.id,
    #         UserProjectEntity.id,
    #         UserEntity.id,
    #         UserProjectEntity.user_id,
    #         UserProjectEntity.project_id,
    #         TaskEntity.task_name,
    #         UserTaskEntity.id,
    #         UserEntity.id,
    #         UserTaskEntity.user_id,
    #         UserTaskEntity.task_id
    #     ).join(
    #         UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
    #     ).join(
    #         ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
    #     ).join(
    #         UserTaskEntity, UserEntity.id == UserTaskEntity.user_id
    #     ).join(
    #         TaskEntity, UserTaskEntity.task_id == TaskEntity.id
    #     ).where(
    #         ProjectEntity.project_name == self.project_name_list,
    #         TaskEntity.task_name == self.task_name_list,
    #         UserTaskEntity.user_id==self.user_id
    #     ))
    #     user_in_task_exist = user_in_task_exist.fetchone()
    #     if user_in_task_exist != None:
    #         logger.success("successfuly showed list of comments in a task")

    #         task_id = user_in_task_exist[1]
    #         task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
    #         task = task.scalars().one_or_none()

    #         projects_data = [
    #         {
    #             comment.comment_name,
    #         }
    #         for comment in task.comments
    #         ]

    #         return projects_data

    #     else:
    #         logger.warning(f"{tname} task doesn't have any comments")
    #         # print("dose not this task")
    #         print("This task doesn't have comment")
    #         return False

    def list_comment(self, pname, tname):
        """This function shows list of comments in a task (if task exists)"""
        try:
            self.user_id = self.user.get_id_user_login()
            self.project_name_list = pname
            self.task_name_list = tname

            user_in_task_exist = self.session.execute(
                select(
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
                    UserTaskEntity.user_id == self.user_id
                )
            )
            user_in_task_exist = user_in_task_exist.fetchone()

            if user_in_task_exist is not None:
                logger.success("Successfully showed list of comments in a task")

                task_id = user_in_task_exist[1]
                task = self.session.execute(select(TaskEntity).filter_by(id=task_id))
                task = task.scalars().one_or_none()

                if task is None:
                    logger.error(f"Task with id {task_id} not found")
                    return "Task not found"

                projects_data = [
                    {
                        "comment_name": comment.comment_name,
                    }
                    for comment in task.comments
                ]

                return projects_data
            else:
                logger.warning(f"{tname} task doesn't have any comments")
                print("This task doesn't have comments")
                return False
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    # def create_task(self, add_task_to_which_project: str, task_name: str, task_description: str) -> str:
    #     """This function takes needed argumants and creates tasks. (a project can't have two task with the same name)"""

    #     self.user_id = self.user.get_id_user_login() 
    #     self.project_name = add_task_to_which_project
    #     project_name_exist = self.session.execute(select(
    #         ProjectEntity.project_name,
    #         ProjectEntity.id.label("project_id"),
    #         UserProjectEntity.id,
    #         UserEntity.id,
    #         UserProjectEntity.user_id,
    #         UserProjectEntity.project_id
    #     ).join(
    #         UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
    #     ).join(
    #         ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
    #     ).where(
    #         ProjectEntity.project_name == self.project_name,
    #         UserProjectEntity.user_id == self.user_id
    #     ))
        
    #     project_name_exist = project_name_exist.fetchone()

    #     if project_name_exist == None:
    #         logger.warning(f"User doesn't have project {add_task_to_which_project} ")

    #         return "You don't have a project with this name!"
    #     else:
            
    #         self.project_id = project_name_exist[1]
    #         self.task_name = task_name
    #         self.task_description = task_description
            
    #         if True:
    #             leader = self.session.execute(select(LeaderEntity).filter(LeaderEntity.project_id==self.project_id,LeaderEntity.user_id==self.user_id))
    #             leader = leader.scalars().one_or_none()
    #             self.leader_id =leader.id
                

    #             exist_task = self.session.execute(
    #                 select(TaskEntity).where(
    #                     TaskEntity.project_id == self.project_id,
    #                     TaskEntity.task_name == self.task_name
    #                 )
    #             )
    #             exist_task = exist_task.scalars().one_or_none()
    #             # print(exist_task)
    #             if exist_task == None or exist_task == []:
    #                 logger.success("Task made successfuly")

    #                 db_model = TaskEntity(task_name=self.task_name,task_description=self.task_description,
    #                                       project_id=self.project_id,leader_id = self.leader_id)
    #                 self.session.add(db_model)
    #                 self.session.commit()
    #                 self.session.refresh(db_model)
    #                 return "Task Made Successfully"
    #             else:
    #                 logger.warning(f"project {add_task_to_which_project} already has task {task_name}")

    #                 return "this project has this task"

    def create_task(self, add_task_to_which_project: str, task_name: str, task_description: str) -> str:
        """This function takes needed arguments and creates tasks. (a project can't have two tasks with the same name)"""
        try:
            self.user_id = self.user.get_id_user_login() 
            self.project_name = add_task_to_which_project
            
            project_name_exist = self.session.execute(
                select(
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
                )
            )
            
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is None:
                logger.warning(f"User doesn't have project {add_task_to_which_project} ")
                return "You don't have a project with this name!"
            else:
                self.project_id = project_name_exist[1]
                self.task_name = task_name
                self.task_description = task_description
                
                leader = self.session.execute(
                    select(LeaderEntity).filter(
                        LeaderEntity.project_id == self.project_id,
                        LeaderEntity.user_id == self.user_id
                    )
                )
                leader = leader.scalars().one_or_none()
                
                if leader is not None:
                    exist_task = self.session.execute(
                        select(TaskEntity).where(
                            TaskEntity.project_id == self.project_id,
                            TaskEntity.task_name == self.task_name
                        )
                    )
                    exist_task = exist_task.scalars().one_or_none()
                    
                    if exist_task is None or exist_task == []:
                        logger.success("Task made successfully")

                        db_model = TaskEntity(
                            task_name=self.task_name,
                            task_description=self.task_description,
                            project_id=self.project_id,
                            leader_id=leader.id
                        )
                        self.session.add(db_model)
                        self.session.commit()
                        self.session.refresh(db_model)
                        return "Task Made Successfully"
                    else:
                        logger.warning(f"Project {add_task_to_which_project} already has task {task_name}")
                        return "This project already has this task"
                else:
                    logger.warning(f"You are not the leader of project {add_task_to_which_project}")
                    
                    return "You are not the leader of this project"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    # def add_comment_to_task(self, project_name_add_comment: str, task_name_add_comment: str, comment: str) -> str:
        """This function takes needed argumants and adds comment to task."""

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
            logger.warning("user isn't member of project so he can't add a comment to it")

            return "you are not in a project with this name!"

        else:
            project_id = project_name_exist[1]
            task_exist = self.session.execute(select(TaskEntity).where(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_comment))
            task_exist = task_exist.scalars().one_or_none()
            if task_exist == None:
                logger.warning(f"{project_name_add_comment} project doesn't have {task_name_add_comment} task")
                # print("this project dose not task with this task name!")
                return "this project dosn't have task with this name!"

            else:
                logger.success("Comment added to task successfuly")

                comment = CommentEntity(comment_name=self.comment,project_id=project_id,user_id=self.user_id,task_id=task_exist.id)
                self.session.add(comment)
                self.session.commit()
                self.session.refresh(comment)
                return "Comment Added succesfully"

    def add_comment_to_task(self, project_name_add_comment: str, task_name_add_comment: str, comment: str) -> str:
        """This function takes needed arguments and adds a comment to a task."""
        try:
            self.user_id = self.user.get_id_user_login()
            self.project_name_add_comment = project_name_add_comment
            self.task_name_add_comment = task_name_add_comment
            self.comment = comment

            project_name_exist = self.session.execute(
                select(
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
                    UserProjectEntity.user_id == self.user_id
                )
            )

            project_name_exist = project_name_exist.fetchone()
            
            if project_name_exist is None:
                logger.warning("User isn't a member of the project so they can't add a comment to it")
                return "You are not in a project with this name!"
            else:
                project_id = project_name_exist[1]
                task_exist = self.session.execute(
                    select(TaskEntity).where(
                        TaskEntity.project_id == project_id,
                        TaskEntity.task_name == self.task_name_add_comment
                    )
                )
                task_exist = task_exist.scalars().one_or_none()
                
                if task_exist is None:
                    logger.warning(f"{project_name_add_comment} project doesn't have {task_name_add_comment} task")
                    return "This project doesn't have a task with this name!"
                else:
                    logger.success("Comment added to task successfully")

                    comment = CommentEntity(
                        comment_name=self.comment,
                        project_id=project_id,
                        user_id=self.user_id,
                        task_id=task_exist.id
                    )
                    self.session.add(comment)
                    self.session.commit()
                    self.session.refresh(comment)
                    return "Comment Added successfully"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    # def add_user_to_task(self, pname: str, tname: str, uname: str) -> str:
        """This function takes needed argumants and adds task to user."""

        self.user_id=self.user.get_id_user_login()
        self.project_name_add_user = pname
        self.task_name_add_user = tname
        self.user_add_user = uname

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
            logger.warning(f"leader doesn't have {pname} project")

            return "you dont have project with this name!"
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_user))
            task=task.scalars().one_or_none()
            if task==None:
                logger.warning(f"{pname} project doesn't have {tname} task")

                return "This Project Doesn't Have This Task"
            else:

                user_exsit = self.session.execute(select(UserEntity).filter_by(username = self.user_add_user))
                user_exsit = user_exsit.scalars().one_or_none()
                if user_exsit == None:
                    logger.warning(f"{uname} user doesn't have account")

                    return "This user dosnt have account"
                else:
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
                        logger.warning(f"{uname} user has already been added to {tname} task")

                        return "This user has already been added to your task"
                    else:
                        logger.success(f"{uname} user added to {tname} task successfuly")
                        
                        user_exsit.tasks.append(task)
                        self.session.commit()
                        return "Successful"
                
    def add_user_to_task(self, pname: str, tname: str, uname: str) -> str:
        """This function takes needed arguments and adds a task to a user."""
        try:
            self.user_id = self.user.get_id_user_login()
            self.project_name_add_user = pname
            self.task_name_add_user = tname
            self.user_add_user = uname

            project_name_exist = self.session.execute(
                select(
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
                )
            )
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is None:
                logger.warning(f"Leader doesn't have {pname} project")
                return "You don't have a project with this name!"
            else:
                project_id = project_name_exist[1]
                task = self.session.execute(
                    select(TaskEntity).filter(
                        TaskEntity.project_id == project_id,
                        TaskEntity.task_name == self.task_name_add_user
                    )
                )
                task = task.scalars().one_or_none()
                
                if task is None:
                    logger.warning(f"{pname} project doesn't have {tname} task")
                    return "This Project Doesn't Have This Task"
                else:
                    user_exist = self.session.execute(
                        select(UserEntity).filter_by(username=self.user_add_user)
                    )
                    user_exist = user_exist.scalars().one_or_none()
                    
                    if user_exist is None:
                        logger.warning(f"{uname} user doesn't have an account")
                        return "This user doesn't have an account"
                    else:
                        user_in_task_exist = self.session.execute(
                            select(
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
                                UserTaskEntity.user_id == user_exist.id
                            )
                        )
                        user_in_task_exist = user_in_task_exist.fetchone()

                        if user_in_task_exist is not None:
                            logger.warning(f"{uname} user has already been added to {tname} task")
                            return "This user has already been added to your task"
                        else:
                            logger.success(f"{uname} user added to {tname} task successfully")
                            user_exist.tasks.append(task)
                            self.session.commit()
                            return "Successful"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

