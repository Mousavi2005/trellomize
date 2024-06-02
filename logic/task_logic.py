import argparse
from sqlalchemy import select, Column, delete
from model.base_entity import TaskEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
from sqlalchemy.sql import text
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from model.base_entity import ProjectEntity,UserProjectEntity, UserEntity,LeaderEntity, CommentEntity, UserTaskEntity, StatusEnum, PriorityEnum, Task_History
import psycopg2
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

    def list_users(self, pname: str, tname: str) -> Union[str, list, bool]:
        """This function returns list of users in task"""
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

                userss_data = [
                    {
                        'username' : user.username,
                    }
                    for user in task.users
                ]

                
                formatted_u_data = [
                    f"Username: {u['username']}"
                    for u in userss_data
                ]


                return formatted_u_data
            else:
                logger.warning(f"{tname} task doesn't have any users")
                # print("This task doesn't have users")
                return False
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def list_comment(self, pname: str, tname: str) -> Union[str, list, bool]:
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

                comments_data = [
                    {
                        'Comment' : comment.comment_name,
                    }
                    for comment in task.comments
                ]

                formatted_c_data = [
                    f"Comment: {c['Comment']}"
                    for c in comments_data
                ]

                return formatted_c_data
            else:
                logger.warning(f"{tname} task doesn't have any comments")
                return False
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def create_task(self, pname: str, tname: str, description: str, priority: str, status: str, finish_date: int) -> Union[str, None]:
        if not isinstance(string_to_int(finish_date), int) :
            # print(finish_date)
            # print(type(finish_date))
            return "invalid finish date.Enter days you want to finsh the task"
        if status == "":
            status = "BACKLOG"
        if priority =="":
            priority = "LOW"

        self.user_id = self.user.get_id_user_login()
        self.task_name = tname
        self.project_name = pname
        self.task_status = status
        self.task_priority = priority
        self.task_description = description

        if self.task_status not in StatusEnum or self.task_priority not in PriorityEnum:
            return "task_status or task_priority invalid"
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
                    # return self.user_id
                    print('Error')
            else:
                
                self.project_id = project_name_exist[1]
                
                if True:
                    leader = self.session.execute(select(LeaderEntity).filter(LeaderEntity.project_id==self.project_id,LeaderEntity.user_id==self.user_id))
                    leader = leader.scalars().one_or_none()
                    self.leader_id =leader.id
                    userid = leader.user_id
                    userr = self.session.execute(select(UserEntity).filter_by(id=userid))
                    userr = userr.scalars().one_or_none()
                    

                    exist_task = self.session.execute(
                        select(TaskEntity).where(
                            TaskEntity.project_id == self.project_id,
                            TaskEntity.task_name == self.task_name
                        )
                    )
                    exist_task = exist_task.scalars().one_or_none()
                    if exist_task == None or exist_task == []:
                        db_model = TaskEntity(task_priority=self.task_priority,task_status=self.task_status,task_name=self.task_name,task_description=self.task_description,
                                            project_id=self.project_id,leader_id = self.leader_id, finish_date=finish_date)
                        userr.tasks.append(db_model)
                        self.session.add(db_model)
                        self.session.commit()
                        self.session.refresh(db_model)
                        return "Task Made Successfully"
                    else:
                        return "this project has this task"

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

    def add_user_to_task(self, pname: str, tname: str, uname:str) -> str:
        """This function takes needed argument and adds a user to task"""

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
            return "you dont have project with this name!"
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==self.task_name_add_user))
            task=task.scalars().one_or_none()
            if task==None:
                return "This Project Doesn't Have This Task"
            else:
                user_exsit = self.session.execute(select(UserEntity).filter_by(username = self.user_add_user))
                user_exsit = user_exsit.scalars().one_or_none()
                if user_exsit == None or user_exsit==[]:
                    return "This user dosn't have account or isn't in this project"
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
                    return "This user dosn't have account or isn't in this project"
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
                        return "This user has already been added to your task"
                    else:
                        user_exsit.tasks.append(task)
                        self.session.commit()
                        return "Successful"

    def edit_task(self, pname: str, tname: str, ppriority: str, sstatus: str, description: str):
        """This function takes needed argument and edits a task"""
        self.user_id=self.user.get_id_user_login()
        if ppriority == "" :
            ppriority = "LOW"
        if sstatus == "":
            sstatus = "BACKLOG"

        user = self.session.execute(select(UserEntity).filter_by(id=self.user_id))
        user = user.scalars().one_or_none()
        project_name = pname
        taskname_name = tname

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
                return "you dont have a project with this name"
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==taskname_name))
            task=task.scalars().one_or_none()
            if task==None:
                return "task dose not exist in this project"
            else:
                user_in_task_exist = self.session.execute(select(UserTaskEntity).where(UserTaskEntity.task_id==task.id,UserTaskEntity.user_id==self.user_id))
                user_in_task_exist = user_in_task_exist.scalars().one_or_none()
                if user_in_task_exist ==None:
                    return "you aren't member of this task!"
                else:
                    temp = 0
                    task_description = description
                    status = sstatus
                    priority = ppriority
                    if task_description!="":
                        task.task_description = task_description
                    if status!="":
                        if status in StatusEnum:
                            task.status = status
                        else:
                            temp += 5
                    if priority!="":
                        if priority in PriorityEnum:
                            task.priority = priority
                        else:
                            temp += 10

                    self.session.commit()
                    task_history = Task_History(edit_description=task.task_description,task_id=task.id,edit_status=task.status,edit_priority=task.priority, username = user.username)
                    self.session.add(task_history)
                    self.session.commit()
                    self.session.refresh(task_history)
                    return temp

    def list_history(self, pname: str, tname: str) -> Union[str, list]:
        """This function takes needed argument and shows history list"""
        
        self.user_id=self.user.get_id_user_login()
        project_name = pname
        taskname_name = tname
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
                return "you dont have a project with this name"
        else:
            project_id = project_name_exist[1]
            task = self.session.execute(select(TaskEntity).filter(TaskEntity.project_id==project_id,TaskEntity.task_name==taskname_name))
            task=task.scalars().one_or_none()
            if task==None:
                return "this task dose not exist in this project"
            else:
                user_in_task_exist = self.session.execute(select(UserTaskEntity).where(UserTaskEntity.task_id==task.id,UserTaskEntity.user_id==self.user_id))
                user_in_task_exist = user_in_task_exist.scalars().one_or_none()
                if user_in_task_exist ==None:
                    return "you not member in this project!"
                else:
                    history = self.session.execute(select(Task_History).filter(Task_History.task_id==task.id))
                    history = history.scalars().all()

                    history_data = [
                        {
                            'Edit status' : his.edit_status.value,
                            'Edit priority' : his.edit_priority.value,
                            'Edit description' : his.edit_description
                        }
                        for his in history
                    ]

                    formatted_h_data = [
                        f"Estatus: {h['Edit status']}, Epriority: {h['Edit priority']}, Edescription: {h['Edit description']}"
                        for h in history_data
                    ]
                    return formatted_h_data

    def delete_user_from_task(self, pname: str, tname: str, uname: str) -> str:
        """This function takes needed argument and deletes a user from task"""
        self.user_id=self.user.get_id_user_login()
        project_name = pname
        task_name = tname
        username = uname
        user_id_for_delete = self.session.execute(select(UserEntity).filter_by(username = username ))
        user_id_for_delete = user_id_for_delete.scalars().one_or_none()
        if user_id_for_delete ==None:
            return "this username dose not exist"
        else:
            delete_user_id = user_id_for_delete.id
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
            ProjectEntity.project_name == project_name,
            UserProjectEntity.user_id == self.user_id
        ))
            project_name_exist = project_name_exist.fetchone()
            if project_name_exist == None:
                return "dose not exist this project"

            else:
                project_id = project_name_exist[1]
                is_leader = self.session.execute(select(LeaderEntity).where(LeaderEntity.user_id==self.user_id,LeaderEntity.project_id==project_id))
                is_leader = is_leader.scalars().one_or_none()
                if is_leader==None or is_leader==[]:
                    return "you are not leader"
                else:
                    user_delete_exist = self.session.execute(select(
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
                ))
                    user_delete_exist = user_delete_exist.fetchone()
                    if user_delete_exist == None:

                        return "this username dose not exist in this project"
                    else:
                        task = self.session.execute(select(TaskEntity).filter(TaskEntity.task_name==task_name,TaskEntity.project_id==project_id))
                        task = task.scalars().one_or_none()
                        if task == None:
                            return "this task dose not exist"
                        else: 
                            user_exist_in_task = self.session.execute(select(UserTaskEntity).filter(UserTaskEntity.user_id==delete_user_id,UserTaskEntity.task_id==task.id))
                            user_exist_in_task = user_exist_in_task.scalars().one_or_none()
                            if user_exist_in_task == None:
                                return "this username dose not exist in this task"
                            else:
                                self.session.execute(delete(UserTaskEntity).filter(UserTaskEntity.user_id == delete_user_id,UserTaskEntity.task_id == task.id))
                                self.session.commit()
                                return 'successful'

def string_to_int(value: str) -> Union[int, None]:
    """This function checks if a string can be converted to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.warning("entered date isn't intiger")
        return None

