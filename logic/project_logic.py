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
engine = create_engine("postgresql://postgres:foxit@localhost/t2")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class project:
    def __init__(self,use=None):
        self.use=use
        self.project_name = None
        self.user_id = None
        self.projec_id = None
        self.session = get_session()
   

    def create_project(self,pname):
        self.user_id = self.use.get_id_user_login()
        print(self.user_id)
        if self.user_id != None:
            user = self.session.execute(select(UserEntity).filter_by(id=self.user_id))
            user = user.scalars().one_or_none()
            # self.create_project_from_input()
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
                # print("this project_name is exist")
                return "this project_name is exist"
                # return False
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
            print("not authentication. you should login or signup")

      
    def create_project_from_input(self):
        self.project_name = input("Enter project name:")
     
    def get_id_project(self):
        return self.projec_id

