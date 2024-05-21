from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic, get_credentials_from_database
from logic.project_logic import project
from logic.task_logic import Tasks
import psycopg2
from psycopg2 import OperationalError
import flet as ft
from rich.console import Console
from logic.project_logic import project


engine = create_engine("postgresql://postgres:foxit@localhost/t2")
Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



def main(page: ft.Page):
    page.title = "Project Management System"
    x = UserLogic()
    y = project(x)

    # Initialize the snackbar with default content
    snackbar = ft.SnackBar(content=ft.Text(""))

    def signup_view(e):
        page.clean()
        username = ft.TextField(label="Username")
        password = ft.TextField(label="Password", password=True)
        signup_button = ft.ElevatedButton(text="Sign Up", on_click=lambda _: signup(username.value, password.value))

        page.add(ft.Column([username, password, signup_button]))
        page.update()

    def signup(username, password):
        if x.signup_user(username, password):
            page.session.set("user", username)
            snackbar.content.value = "Signup successful!"
        else:
            snackbar.content.value = "Username already exists"
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()
        main_menu()

    def login_view(e):
        page.clean()
        username = ft.TextField(label="Username")
        password = ft.TextField(label="Password", password=True)
        login_button = ft.ElevatedButton(text="Log In", on_click=lambda _: login(username.value, password.value))

        page.add(ft.Column([username, password, login_button]))
        page.update()
        # print(x.get_id_user_login())

    def login(username, password):
        if x.login_user(username, password):
            page.session.set("user", username)
            main_menu()
            # print(x.get_id_user_login())

        else:
            snackbar.content.value = "Invalid credentials"
            snackbar.open = True
            page.snack_bar = snackbar
            page.update()

    def main_menu():
        page.clean()
        user = page.session.get("user")
        if user:
            page.add(ft.Text(f"Welcome {user}!"))
        else:
            page.add(ft.Text("Welcome!"))
        create_project_button = ft.ElevatedButton(text="Create Project", on_click=create_project_view)
        page.add(ft.Column([create_project_button]))
        page.update()

    def create_project_view(e):
        page.clean()
        project_name = ft.TextField(label="Project Name")
        create_button = ft.ElevatedButton(text="Create", on_click=lambda _: create_project(project_name.value))
        
        page.add(ft.Column([project_name, create_button]))
        page.update()

    def create_project(project_name):
        user = page.session.get("user")
        # Add your logic to handle project creation here
        massage = y.create_project(project_name)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    # Initial View
    page.add(ft.Column([
        ft.Text("Welcome to Project Management System"),
        ft.ElevatedButton(text="Sign Up", on_click=signup_view),
        ft.ElevatedButton(text="Log In", on_click=login_view),
    ]))
    page.update()

ft.app(target=main)












    
        #   UPDATING DATABASE CODE
# import psycopg2
# # Connect to the database
# conn = psycopg2.connect(
#     dbname="trello",
#     user="postgres",
#     password="foxit",
#     host="localhost",  # Assuming your local PostgreSQL is running on localhost
#     port="5432"  # Default PostgreSQL port
# )
# cursor = conn.cursor()