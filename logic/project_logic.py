from sqlalchemy import select ,and_
from model.base_entity import ProjectEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
# from logic.user_logic import get_credentials_from_database
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import psycopg2
from logic.user_logic import UserLogic
from model.base_entity import UserEntity,UserProjectEntity,LeaderEntity
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

class project:
    def __init__(self,use=None):
        self.use=use
        self.project_name = None
        self.user_id = None
        self.add_username = None
        self.add_project_name = None
        self.projec_id = None
        self.session = get_session()
   

    def create_project(self,pname):
        """This function takes needed argument and creates a project (a user can't have two project with the same name)"""

        self.user_id = self.use.get_id_user_login()
        if self.user_id != None:
            user = self.session.execute(select(UserEntity).filter_by(id=self.user_id))
            user = user.scalars().one_or_none()
            self.project_name = pname

            project_name_exist=self.session.execute(select(
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
            UserProjectEntity.user_id==self.user_id
        ))
           
            project_name_exist = project_name_exist.scalars().all()
            print(project_name_exist)
            if project_name_exist != []:
                logger.warning(f"user already has project {pname}")

                return "this project_name is exist"

            logger.success("Project created successfuly")
            model_project = ProjectEntity(project_name=self.project_name, username=user.username, hash_password=user.hash_password, first_name=user.first_name, last_name=user.last_name)
            model_leader = LeaderEntity()
            user.projects.append(model_project)

            model_leader.project=model_project
            model_leader.user=user


            self.session.add(model_project)
            self.session.add(model_leader)
            self.session.commit()
            self.session.refresh(model_project)
            # self.session.refresh(model_leader)
            # print("create project successfull")
            return "create project successfull"
            
        else:
            logger.critical("We don't have users id")
            print("not authentication. you should login or signup")





    def add_user_to_project(self, uname, pname):
        """This function takes needed argumants and adds user to project"""
        self.user_id = self.use.get_id_user_login()
        self.add_username = uname
        self.add_project_name = pname

        project_name_exist = self.session.execute(select(
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
        ))
        project_name_exist = project_name_exist.fetchone()

        if project_name_exist == None:
            logger.warning(f"leader doesn't have {pname} project")
            # print(self.user_id)
            return "you don't have project with this name!"
        else:
            project_id = project_name_exist[1]
            user_exsit = self.session.execute(select(UserEntity).filter_by(username = self.add_username))
            user_exsit = user_exsit.scalars().one_or_none()
            if user_exsit == None:
                logger.warning(f"user {uname} doesn'd have account")
                # print("The user you want to add to your project does not exist")
                return "The user you want to add to your project does not exist"
            else:
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
            # ProjectEntity.project_name == self.add_project_name,
            ProjectEntity.id == project_id,
            UserProjectEntity.user_id==user_exsit.id
        ))
                project_name_exist = project_name_exist.fetchone()

                model_project = self.session.execute(select(ProjectEntity).filter_by(id=project_id))
                model_project = model_project.scalars().one_or_none()
                if project_name_exist!= None:
                    logger.warning(f"The {uname} has already been added to {pname} project")

                    return "The user has already been added to your project"
                else:
                    logger.success(f"user {uname} added to {pname} project")

                    user_exsit.projects.append(model_project)
                    self.session.commit()
                    return "User Added to project succesfully"

    
    # def input_for_add_project(self):
        # self.add_username = input("Which user to add to your project (username)?")
        # self.add_project_name = input("The name of the project you want the user to be added to?")


    # def create_project_from_input(self):
    #     self.project_name = input("Enter project name:")
     
    def get_id_project(self):
        return self.projec_id

