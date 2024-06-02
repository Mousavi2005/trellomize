from sqlalchemy import select ,and_, delete
from model.base_entity import ProjectEntity, TaskEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import psycopg2
from logic.user_logic import UserLogic
from model.base_entity import UserEntity,UserProjectEntity,LeaderEntity, UserTaskEntity
from loguru import logger
from typing import Union

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

class project:
    def __init__(self,use=None):
        self.use=use
        self.project_name = None
        self.user_id = None
        self.add_username = None
        self.add_project_name = None
        self.projec_id = None
        self.session = get_session()
   

    def create_project(self, pname: str) -> str:
        """This function takes needed argument and creates a project (a user can't have two projects with the same name)"""
        try:
            self.user_id = self.use.get_id_user_login()
            if self.user_id is not None:
                user = self.session.execute(select(UserEntity).filter_by(id=self.user_id))
                user = user.scalars().one_or_none()
                self.project_name = pname

                project_name_exist = self.session.execute(
                    select(
                        ProjectEntity.project_name,
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

                project_name_exist = project_name_exist.scalars().all()

                if project_name_exist:
                    logger.warning(f"user already has project {pname}")
                    return "this project name exists"

                logger.success("Project created successfully")

                model_project = ProjectEntity(
                    project_name=self.project_name, 
                    username=user.username, 
                    hash_password=user.hash_password, 
                    first_name=user.first_name, 
                    last_name=user.last_name
                )
                model_leader = LeaderEntity()
                user.projects.append(model_project)

                model_leader.project = model_project
                model_leader.user = user
                self.session.add(model_project)
                self.session.add(model_leader)
                self.session.commit()
                self.session.refresh(model_project)
                return "create project successful"

            else:
                logger.critical("We don't have user's id")
                return "not authenticated. you should login or signup"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def add_user_to_project(self, uname: str, pname: str) -> str:
        """This function takes needed arguments and adds user to project"""
        try:
            self.user_id = self.use.get_id_user_login()
            self.add_username = uname
            self.add_project_name = pname

            project_name_exist = self.session.execute(
                select(
                    ProjectEntity.project_name,
                    UserProjectEntity.id,
                    UserEntity.id,
                    UserProjectEntity.user_id,
                    UserProjectEntity.project_id
                ).join(
                    UserProjectEntity, UserEntity.id == UserProjectEntity.user_id
                ).join(
                    ProjectEntity, UserProjectEntity.project_id == ProjectEntity.id
                ).where(
                    ProjectEntity.project_name == self.add_project_name,
                    UserProjectEntity.user_id == self.user_id
                )
            )
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is None:
                logger.warning(f"leader doesn't have {pname} project")
                return "you don't have project with this name!"
            else:
                project_id = project_name_exist[1]
                # print(project_id)
                # print("----------------------")
                user_exsit = self.session.execute(select(UserEntity).filter_by(username=self.add_username))
                user_exsit = user_exsit.scalars().one_or_none()
                if user_exsit is None:
                    logger.warning(f"user {uname} doesn't have an account")
                    return "The user you want to add to your project does not exist"
                else:
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
                            ProjectEntity.id == project_id,
                            UserProjectEntity.user_id == user_exsit.id
                        )
                    )
                    project_name_exist = project_name_exist.fetchone()

                    model_project = self.session.execute(select(ProjectEntity).filter_by(id=project_id))
                    model_project = model_project.scalars().one_or_none()
                    # print(model_project)
                    # print("--------------------------")

                    if project_name_exist != None:
                        logger.warning(f"The {uname} has already been added to {pname} project")
                        return "The user has already been added to your project"
                    else:
                        logger.success(f"user {uname} added to {pname} project")
                        user_exsit.projects.append(model_project)
                        self.session.commit()
                        return "User added to project successfully"

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}" 

    def list_tasks(self, pname: str) -> Union[str, list, bool]:
        """This function shows list of project tasks"""
        try:
            self.user_id = self.use.get_id_user_login()
            self.project_name_list = pname

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
                    ProjectEntity.project_name == self.project_name_list,
                    UserProjectEntity.user_id == self.user_id
                )
            )
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is None:
                logger.warning("This project doesn't exist!")
                return False
            else:
                logger.success("List of project tasks shown successfully")

                project_id = project_name_exist[1]

                tasks = self.session.execute(select(TaskEntity).filter_by(project_id=project_id))
                tasks = tasks.scalars().all()

                # tasks_data = [
                #     {
                #         'Task name' : task.task_name,
                #     }
                #     for task in tasks
                # ]

                # formatted_t_data = [
                #     f"Task name: {t['Task name']}"
                #     for t in tasks_data
                # ]

                t_data = [
                {
                    'Name' : task.task_name,
                    'Status' : task.task_status.value,
                    'Priority' : task.task_priority.value,
                    'description' : task.task_description
                }
                for task in tasks
                ]

                formatted_t_data = [
                    f"Name: {task['Name']}, Status: {task['Status']}, Priority: {task['Priority']}, Description: {task['description']}"
                    for task in t_data
                ]



                return formatted_t_data
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def list_users(self, pname: str) -> Union[str, list, bool]:
        """This function returns list of users in a project"""
        try:
            self.user_id = self.use.get_id_user_login()
            self.project_name_list = pname

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
                    ProjectEntity.project_name == self.project_name_list,
                    UserProjectEntity.user_id == self.user_id
                )
            )
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is not None:

                project_id = project_name_exist[1]
                project = self.session.execute(select(ProjectEntity).filter_by(id=project_id))
                project = project.scalars().one_or_none()

                if project is None:
                    logger.error(f"Project with id {project_id} not found")
                    return "Project not found"
                logger.success(f"List of users in {pname} project shown successfully")

                users = project.users

                users_data = [
                    {
                        'username' : user.username,
                    }
                    for user in users
                ]

                formatted_u_data = [
                    f"Username : {u['username']}"
                    for u in users_data
                ]


                return formatted_u_data
            else:
                logger.warning(f"User doesn't have {pname} project")
                return False
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def delete_project(self, pname: str) -> str:
        """This function deletes a project (if user is leader of it)"""
        try:
            self.user_id = self.use.get_id_user_login()
            project_name = pname
            
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
                    ProjectEntity.project_name == project_name,
                    UserProjectEntity.user_id == self.user_id
                )
            )
            project_name_exist = project_name_exist.fetchone()

            if project_name_exist is None:
                logger.warning(f"User doesn't have {pname} project to delete it")
                return "You don't have this project"
            else:
                project_id = project_name_exist[1]
                is_leader = self.session.execute(
                    select(LeaderEntity).where(
                        LeaderEntity.user_id == self.user_id,
                        LeaderEntity.project_id == project_id
                    )
                )
                is_leader = is_leader.scalars().one_or_none()

                if is_leader is None:
                    logger.warning(f"User isn't leader of {pname} project to delete it")
                    return "You are not leader"
                else:
                    logger.success(f"{pname} project deleted successfully")

                    self.session.execute(delete(TaskEntity).where(TaskEntity.project_id == project_id))
                    self.session.commit()

                    # self.session.execute(delete(UserTaskEntity).where(UserTaskEntity.task_id == project_id))
                    # self.session.commit()

                    self.session.execute(delete(LeaderEntity).where(LeaderEntity.project_id == project_id))
                    self.session.commit()

                    self.session.execute(delete(UserProjectEntity).where(UserProjectEntity.project_id == project_id))
                    self.session.commit()
                    
                    self.session.execute(delete(ProjectEntity).where(ProjectEntity.id == project_id))
                    self.session.commit()

                    return "Project deleted successfully"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def delete_user_from_project(self, pname: str, uname: str) -> str:
        """This function deletes a user from a project (if project exists and user is added to it)"""
        try:
            self.user_id = self.use.get_id_user_login()
            project_name = pname
            user_name_for_delete = uname
            
            user_id_for_delete = self.session.execute(
                select(UserEntity).filter_by(username=user_name_for_delete)
            )
            user_id_for_delete = user_id_for_delete.scalars().one_or_none()
            
            if user_id_for_delete is None:
                logger.warning(f"{uname} username doesn't have an account to delete from project")
                return "This username does not exist"

            delete_user_id = user_id_for_delete.id
            
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
                    ProjectEntity.project_name == project_name,
                    UserProjectEntity.user_id == self.user_id
                )
            )
            project_name_exist = project_name_exist.fetchone()
            
            if project_name_exist is None:
                logger.warning(f"User isn't in {pname} project")
                return "You don't have this project"

            project_id = project_name_exist[1]
            
            is_leader = self.session.execute(
                select(LeaderEntity).where(
                    LeaderEntity.user_id == self.user_id,
                    LeaderEntity.project_id == project_id
                )
            )
            is_leader = is_leader.scalars().one_or_none()
            
            if is_leader is None:
                logger.warning(f"User isn't leader of {pname} project")
                return "You are not leader"
            
            user_delete_exist = self.session.execute(
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
                    ProjectEntity.project_name == project_name,
                    UserProjectEntity.user_id == delete_user_id
                )
            )
            user_delete_exist = user_delete_exist.fetchone()
            
            if user_delete_exist is None:
                logger.warning(f"{uname} user isn't in this project")
                return "This username isn't in this project"

            logger.success(f"{uname} user deleted from {pname} project successfully")

            self.session.execute(
                delete(UserProjectEntity).where(
                    UserProjectEntity.project_id == project_id,
                    UserProjectEntity.user_id == delete_user_id
                )
            )
            self.session.commit()
            
            return "User deleted successfully"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def get_id_project(self):
        """This function returns id of user"""
        return self.projec_id

