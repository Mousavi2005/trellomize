from sqlalchemy import select
from model.base_entity import ProjectEntity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, table
from logic.user_logic import get_credentials_from_database
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from logic.user_logic import get_credentials_from_database
import psycopg2

engine = create_engine("postgresql://postgres:foxit@localhost/user")

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
            print("project made succesfully.")

    def create_project_from_input(self):
        project_name = input("Enter project name: ")
        user_name = input("Enter user name: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        hash_password = input("Enter password: ")
        credentials = get_credentials_from_database('users')
        # print(get_credentials_from_database("users"))
        temp = 0
        for key, value in credentials.items():
            if key == user_name and value == hash_password:
                self.create_project(project_name, user_name, first_name, last_name, hash_password)
                # print("Project made successfully ")
                temp = 1
                break
        if temp == 0:
            print("You entered username or password wrong. Try again: ")


def project_menu():
    console = Console()
    while True:
        choice = 0
        console.print("1. [bold green]Create new Project[/bold green] ")
        console.print("2. [bold blue]Add user to project[/bold blue] ")
        console.print("3. [bold yellow]Add task to project[/bold yellow] ")
        console.print("4. [bold red]Exit[/bold red] ")
        choice = input("Enter your choice: ")

        if choice == '1' :
            project1 = project()
            # print("Project made successfully ")

        elif choice == '2' :
            username = Prompt.ask("[bold cyan]Enter your username: [/bold cyan]")
            users = get_credentials_from_database('users')
            if username not in users.keys():
                console.print("[bold red]This user doesn't have account on trellomoize[/bold red]")
            else:
            # have to add this user name to project
            # project creator cannot add himself to project
                console.print("[bold green]user added to project.[/bold green]")
        elif choice == '3' :
            pass

        elif choice == '4' :
            console.print("[bold red]Good bye.[/bold red]")
            break
        else :
            console.print("[bold red]Please choose between options: [/bold red]")
        

def delet_project():
    console = Console()
    pname = input("Enter project name: ")
    conn = psycopg2.connect(
        dbname="trello",
        user="postgres",
        password="foxit",
        host="localhost",
        port="5432"  
    )

    cur = conn.cursor()

    project_name_to_delete = pname

    select_query = "SELECT COUNT(*) FROM projects WHERE project_name = %s;"

    cur.execute(select_query, (project_name_to_delete,))
    row_count = cur.fetchone()[0]

    if row_count > 0:
        decision = Prompt.ask('[bold red]Are you sure? (yes/no)  : [/bold red]')
        if decision == 'yes' :
            delete_query = "DELETE FROM projects WHERE project_name = %s;"
            cur.execute(delete_query, (project_name_to_delete,))
            conn.commit()
            console.print("[bold green]Project deleted successfully.[/bold green]")
        else :
            pass
    else:
        console.print("[bold red]Project does not exist. you may have entered project name wrong.[/bold red]")

    cur.close()
    conn.close()


 