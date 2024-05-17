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
engine = create_engine("postgresql://postgres:postgres@localhost/trello")

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
   

    def create_project(self):
        self.user_id = self.use.get_id_user_login()
        print(self.user_id)
        if self.user_id != None:
            user = self.session.execute(select(UserEntity).filter_by(id=self.user_id))
            user = user.scalars().one_or_none()
            self.create_project_from_input()

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
                print("this project_name is exist")
                return False
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
            print("create project successfull")
            
        else:
            print("not authentication. you should login or signup")

      
    def create_project_from_input(self):
        self.project_name = input("Enter project name:")
     
    def get_id_project(self):
        return self.projec_id
# def project_menu():
#     console = Console()
#     while True:
#         choice = 0
#         console.print("1. [bold green]Create new Project[/bold green] ")
#         console.print("2. [bold blue]Add user to project[/bold blue] ")
#         console.print("3. [bold yellow]Add task to project[/bold yellow] ")
#         console.print("4. [bold red]Exit[/bold red] ")
#         choice = input("Enter your choice: ")

#         if choice == '1' :
#             project1 = project()
#             # print("Project made successfully ")

#         elif choice == '2' :
#             username = Prompt.ask("[bold cyan]Enter your username: [/bold cyan]")
#             users = get_credentials_from_database('users')
#             if username not in users.keys():
#                 console.print("[bold red]This user doesn't have account on trellomoize[/bold red]")
#             else:
#             # have to add this user name to project
#             # project creator cannot add himself to project
#                 console.print("[bold green]user added to project.[/bold green]")
#         elif choice == '3' :
#             pass

#         elif choice == '4' :
#             console.print("[bold red]Good bye.[/bold red]")
#             break
#         else :
#             console.print("[bold red]Please choose between options: [/bold red]")
        

# def delet_project():
#     console = Console()
#     pname = input("Enter project name: ")
#     conn = psycopg2.connect(
#         dbname="trello",
#         user="postgres",
#         password="postgres",
#         host="localhost",
#         port="5432"  
#     )

#     cur = conn.cursor()

#     project_name_to_delete = pname

#     select_query = "SELECT COUNT(*) FROM projects WHERE project_name = %s;"

#     cur.execute(select_query, (project_name_to_delete,))
#     row_count = cur.fetchone()[0]

#     if row_count > 0:
#         decision = Prompt.ask('[bold red]Are you sure? (yes/no)  : [/bold red]')
#         if decision == 'yes' :
#             delete_query = "DELETE FROM projects WHERE project_name = %s;"
#             cur.execute(delete_query, (project_name_to_delete,))
#             conn.commit()
#             console.print("[bold green]Project deleted successfully.[/bold green]")
#         else :
#             pass
#     else:
#         console.print("[bold red]Project does not exist. you may have entered project name wrong.[/bold red]")

#     cur.close()
#     conn.close()

# # def get_credentials_from_database3(table_name):
# #     try:
# #         session = get_session()
# #         credentials = session.query(ProjectEntity).all()
# #         credentials_dict = {credential.username: credential.id for credential in credentials}
# #         session.close()
# #         return credentials_dict
# #     except Exception as e:
# #         print("Error while fetching data from database:", e)

# def get_user_credentials():
#     try:
#         # Create engine and session
#         eengine = create_engine("postgresql://postgres:foxit@localhost/t2")
#         Session = sessionmaker(bind=engine)
#         session = Session()

#         # Query to fetch usernames and passwords
#         projects = session.query(ProjectEntity).all()

#         # Close the session
#         session.close()

#         # Convert to dictionary
#         credentials = {p.project_name: p.username for p in projects}
#         return credentials
#     except Exception as e:
#         print("Error while fetching data from database:", e)


 
