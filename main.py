from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic, get_credentials_from_database, get_credentials_from_database_gmail
from logic.project_logic import project
from logic.task_logic import Tasks
from logic.manager_logic import ban_user, activate_user, delet_user, check_deleted_user
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



# def main(page: ft.Page):
#     page.title = "Project Management System"
#     x = UserLogic()
#     y = project(x)
#     z = Tasks(y,x)

#     # Initialize the snackbar with default content
#     snackbar = ft.SnackBar(content=ft.Text(""))

#     def signup_view(e):
#         page.clean()
#         username = ft.TextField(label="Username")
#         gmail = ft.TextField(label="Gmail")
#         password = ft.TextField(label="Password", password=True)
#         signup_button = ft.ElevatedButton(text="Sign Up", on_click=lambda _: signup(username.value, gmail.value, password.value))

#         page.add(ft.Column([username, gmail, password, signup_button]))
#         page.update()

#     def signup(username, gmail, password):

#         if x.signup_user(username, gmail, password) == True :
#             page.session.set("user", username)
#             snackbar.content.value = "Signup successful!"
#             main_menu()
#         elif x.signup_user(username, gmail, password) == "NVG":
#            snackbar.content.value = "Please Enter Valid Gmail" 

#         elif  x.signup_user(username, gmail, password) == "UG":
#            snackbar.content.value = "This Gmail Has Account.Plese Enter Another One" 

#         else:
#             snackbar.content.value = "Username already exists"
#         snackbar.open = True
#         page.snack_bar = snackbar
#         page.update()
#         # main_menu()

#     def login_view(e):
#         page.clean()
#         username = ft.TextField(label="Username")
#         password = ft.TextField(label="Password", password=True)
#         login_button = ft.ElevatedButton(text="Log In", on_click=lambda _: login(username.value, password.value))

#         page.add(ft.Column([username, password, login_button]))
#         page.update()
#         # print(x.get_id_user_login())

#     def login(username, password):
#         if x.login_user(username, password) == "Admin":
#             snackbar.content.value = "login successful admin"
#             admin_menu()

#         elif x.login_user(username, password) == True:
#             page.session.set("user", username)
#             snackbar.content.value = "login successful!"
#             main_menu()
#         elif x.login_user(username, password) == "NA":
#             snackbar.content.value = "Unfortunetly you are baned. please contact adminastrator"

#         else:
#             snackbar.content.value = "Invalid credentials"
#         snackbar.open = True
#         page.snack_bar = snackbar
#         page.update()

#     def main_menu():
#         page.clean()
#         user = page.session.get("user")
#         if user:
#             page.add(ft.Text(f"Welcome {user}!"))
#         else:
#             page.add(ft.Text("Welcome!"))
#         create_project_button = ft.ElevatedButton(text="Create Project", on_click=create_project_view)
#         create_task_button = ft.ElevatedButton(text="Create Task",on_click=create_task_view)
#         add_user_to_project_button = ft.ElevatedButton(text="Add User To Project",on_click=add_user_to_project_view)

#         page.add(ft.Column([create_project_button]))
#         page.add(ft.Column([create_task_button]))
#         page.add(ft.Column([add_user_to_project_button]))
#         page.update()


#     def admin_menu():
#         page.clean()
#         page.add(ft.Text("Welcome Admin!"))

#         ban_user_button = ft.ElevatedButton(text="Ban a user", on_click=ban_user_view)
#         activate_user_button = ft.ElevatedButton(text="Activate a user", on_click=activate_user_view)
#         delete_user_button = ft.ElevatedButton(text="Delete a user", on_click=delete_user_view)

#         page.add(ft.Column([ban_user_button]))
#         page.add(ft.Column([activate_user_button]))
#         page.add(ft.Column([delete_user_button]))
#         page.update()

#     def ban_user_view(e):
        
#         page.clean()
#         username = ft.TextField(label="Username you want to ban")
#         # ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: ban_user(username.value))
#         ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: store_ban_result(username.value))
        
#         page.add(ft.Column([username, ban_button]))
#         page.update()

#     def store_ban_result(username):
#         massage = ban_user(username)
#         # print(massage)
#         # Store the ban result here or perform any further actions
#         snackbar.content.value = massage
#         snackbar.open = True
#         page.snack_bar = snackbar
#         admin_menu()
#         page.update()

#     def activate_user_view(e):
#         page.clean()
#         username = ft.TextField(label="Username you want to activate")
#         activate_button = ft.ElevatedButton(text="Activate", on_click=lambda _: store_activate_result(username.value))

#         page.add(ft.Column([username, activate_button]))
#         page.update()

#     def store_activate_result(username):
#         massage = activate_user(username)
#         # print(massage)
#         # Store the ban result here or perform any further actions
#         snackbar.content.value = massage
#         snackbar.open = True
#         page.snack_bar = snackbar
#         admin_menu()
#         page.update()

#     def delete_user_view(e):

#         page.clean()
#         username = ft.TextField(label="Username you want to delet")
#         activate_button = ft.ElevatedButton(text="Delet", on_click=lambda _: store_delet_resualt(username.value))

#         page.add(ft.Column([username, activate_button]))
#         page.update()

#     def store_delet_resualt(username):
#         massage = delet_user(username)
        
#         snackbar.content.value = massage
#         snackbar.open = True
#         page.snack_bar = snackbar
#         admin_menu()
#         page.update()

#     def create_project_view(e):
#         page.clean()
#         project_name = ft.TextField(label="Project Name")
#         create_button = ft.ElevatedButton(text="Create", on_click=lambda _: create_project(project_name.value))
        
#         page.add(ft.Column([project_name, create_button]))
#         page.update()

#     def create_project(project_name):
#         user = page.session.get("user")
#         # Add your logic to handle project creation here
#         massage = y.create_project(project_name)
#         snackbar.content.value = massage
#         snackbar.open = True
#         page.snack_bar = snackbar
#         main_menu()
#         page.update()

#     def create_task_view(e):
#         page.clean()
#         add_task_to_which_project = ft.TextField(label="this task adds to which project?")
#         task_name = ft.TextField(label="Task Name")
#         task_description = ft.TextField(label="Task Description")
#         create_button = ft.ElevatedButton(text="Create", on_click=lambda _: create_task(add_task_to_which_project.value, task_name.value, task_description.value))
        
#         page.add(ft.Column([add_task_to_which_project, task_name, task_description, create_button]))
#         page.update()

#     def create_task(add_task_to_which_project,task_name, task_description):
#         user = page.session.get("user")
#         # Add your logic to handle task creation here
#         massage = z.create_task(add_task_to_which_project, task_name, task_description)
#         # message = y.create_task(task_name, task_description)
#         snackbar.content.value = massage
#         snackbar.open = True
#         page.snack_bar = snackbar
#         main_menu()
#         page.update()

#     def add_user_to_project_view(e):
#         page.clean()
#         username_for_adding_to_project = ft.TextField(label="Username To Add To Project")
#         project_name_for_adding_user = ft.TextField(label="Project Name For Adding User To")

#         add_button = ft.ElevatedButton(text="Add", on_click=lambda _: add_user_to_project(username_for_adding_to_project.value,project_name_for_adding_user.value))

 
#         page.add(ft.Column([username_for_adding_to_project, project_name_for_adding_user, add_button]))
#         page.update()

#     def add_user_to_project(uname, pname):
        
#         user = page.session.get("user")
#         # Add your logic to handle task creation here
#         massage = y.add_user_to_project(uname, pname)
#         # message = y.create_task(task_name, task_description)
#         snackbar.content.value = massage
#         print(massage)
#         snackbar.open = True
#         page.snack_bar = snackbar
#         main_menu()
#         page.update()

#     # Initial View
#     page.add(ft.Column([
#         ft.Text("Welcome to Project Management System"),
#         ft.ElevatedButton(text="Sign Up", on_click=signup_view),
#         ft.ElevatedButton(text="Log In", on_click=login_view),
#     ]))
#     page.update()

# ft.app(target=main)



