from sqlalchemy import select, text, update
from model.base_entity import UserEntity
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from model.base_entity import ProjectEntity

engine = create_engine("postgresql://postgres:foxit@localhost/trello")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
  


class project:

    def __init__(self):
        self.session = get_session()

    def create_project(self,project_name=input("Enter project name:"),user_name=input("Enter user name:"),first_name=input("Enter first name:"),last_name = input("Enter last name:"),hash_password= input("Enter password")):
        # print(self.session)
        project = self.session.execute(select(ProjectEntity).filter_by(project_name=project_name))

        result_edited = project.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("project is exist")
        else:
            db_model = ProjectEntity(project_name=project_name,username=user_name,hash_password=hash_password,first_name=first_name,last_name=last_name)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)



