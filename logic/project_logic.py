from sqlalchemy import select
from model.base_entity import ProjectEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from logic.user_logic import get_credentials_from_database

engine = create_engine("postgresql://postgres:foxit@localhost/trello")

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class project:
    def __init__(self):
        self.session = get_session()
        self.create_project_from_input()

    def create_project(self, project_name, user_name, first_name, last_name, hash_password):
        project = self.session.execute(select(ProjectEntity).filter_by(project_name=project_name))

        result_edited = project.scalars().one_or_none()
        print(result_edited)
        if result_edited:
            print("project is exist")
        else:
            db_model = ProjectEntity(project_name=project_name, username=user_name, hash_password=hash_password, first_name=first_name, last_name=last_name)
            self.session.add(db_model)
            self.session.commit()
            self.session.refresh(db_model)

    def create_project_from_input(self):
        project_name = input("Enter project name:")
        user_name = input("Enter user name:")
        first_name = input("Enter first name:")
        last_name = input("Enter last name:")
        hash_password = input("Enter password:")
        credentials = get_credentials_from_database('users')
        # print(get_credentials_from_database("users"))
        temp = 0
        for key, value in credentials.items():
            if key == user_name and value == hash_password:
                self.create_project(project_name, user_name, first_name, last_name, hash_password)
                print("Project made successfully ")
                temp = 1
                break
        if temp == 0:
            print("You entered username or password wrong. Try again: ")
        






# from sqlalchemy import select, text, update
# from model.base_entity import UserEntity
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from model.base_entity import ProjectEntity

# engine = create_engine("postgresql://postgres:foxit@localhost/trello")

# def get_session():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session
  


# class project:

#     def __init__(self):
#         self.session = get_session()

#     def create_project(self,project_name=input("Enter project name:"),user_name=input("Enter user name:"),first_name=input("Enter first name:"),last_name = input("Enter last name:"),hash_password= input("Enter password")):
#         # print(self.session)
#         project = self.session.execute(select(ProjectEntity).filter_by(project_name=project_name))

#         result_edited = project.scalars().one_or_none()
#         print(result_edited)
#         if result_edited:
#             print("project is exist")
#         else:
#             db_model = ProjectEntity(project_name=project_name,username=user_name,hash_password=hash_password,first_name=first_name,last_name=last_name)
#             self.session.add(db_model)
#             self.session.commit()
#             self.session.refresh(db_model)

