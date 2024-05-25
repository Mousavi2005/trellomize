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
from loguru import logger


engine = create_engine("postgresql://postgres:foxit@localhost/t2")
Base.metadata.create_all(engine)
logger.add(
    "file1",
    format="{time} {level} {message}",
    rotation="1 MB"
)


def get_session():
    logger.info("A session created")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def main(page: ft.Page):
    page.clean()
    """Flet function to open a page"""
    logger.info("Openning main page")
    page.title = "Project Management System"
    x = UserLogic()
    y = project(x)
    z = Tasks(y,x)

    # Initialize the snackbar with default content
    snackbar = ft.SnackBar(content=ft.Text(""))

    def signup_view(e):
        """Opens signup menu in flet"""
        logger.debug("openning signup menu")
        page.clean()
        username = ft.TextField(label="Username")
        gmail = ft.TextField(label="Gmail")
        password = ft.TextField(label="Password", password=True)
        signup_button = ft.ElevatedButton(text="Sign Up", on_click=lambda _: signup(username.value, gmail.value, password.value))

        page.add(ft.Column([username, gmail, password, signup_button]))
        page.update()

    def signup(username, gmail, password):
        """This finctions takes needed arguments and adds user to database (username and gmail must be unique and valid)"""
        logger.debug(f"Attempting to sign up user: {username}")

        if x.signup_user(username, gmail, password) == True :
            page.session.set("user", username)
            snackbar.content.value = "Signup successful!"
            main_menu()
        elif x.signup_user(username, gmail, password) == "NVG":
            snackbar.content.value = "Please Enter Valid Gmail" 

        elif  x.signup_user(username, gmail, password) == "UG":
            snackbar.content.value = "This Gmail Has Account.Plese Enter Another One" 

        else:
            snackbar.content.value = "Username already exists"
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()
        # main_menu()

    def login_view(e):
        """Opens login menu in flet"""
        logger.debug("Opening login menu")
        page.clean()
        username = ft.TextField(label="Username")
        password = ft.TextField(label="Password", password=True)
        login_button = ft.ElevatedButton(text="Log In", on_click=lambda _: login(username.value, password.value))

        page.add(ft.Column([username, password, login_button]))
        page.update()
        # print(x.get_id_user_login())

    def login(username, password):
        """This function takes needed arguments and connects user to database (if user diesnt have account they have to signup first)"""
        logger.debug(f"Attempting to login user: {username}")

        if x.login_user(username, password) == "Admin":
            # logger.success(f"login successful for admin: {username}")
            snackbar.content.value = "login successful admin"
            admin_menu()

        elif x.login_user(username, password) == True:
            # logger.success(f"login successful for user: {username}")

            page.session.set("user", username)
            snackbar.content.value = "login successful!"
            main_menu()

        elif x.login_user(username, password) == "NA":
            # logger.warning(f"user : {username} is baned!")
            snackbar.content.value = "Unfortunetly you are baned. please contact adminastrator"

        else:
            # logger.warning(f"username : {username} and password: {password} are incorrect!")
            snackbar.content.value = "Invalid credentials"
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()

    def main_menu():
        """This function opens the main menu in flet"""
        logger.debug("Opening main menu")
        page.clean()
        user = page.session.get("user")
        if user:
            page.add(ft.Text(f"Welcome {user}!"))
        else:
            page.add(ft.Text("Welcome!"))

        # back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=signout_view)
        create_project_button = ft.ElevatedButton(text="Create Project", on_click=create_project_view)
        create_task_button = ft.ElevatedButton(text="Create Task",on_click=create_task_view)
        add_user_to_project_button = ft.ElevatedButton(text="Add User To Project",on_click=add_user_to_project_view)
        add_comment_to_task_button = ft.ElevatedButton(text="Add Comment To Task",on_click=add_comment_to_task_view)
        add_user_to_task_button = ft.ElevatedButton(text="Add User To Task", on_click=add_user_to_task_view)
        sighn_out_button = ft.ElevatedButton(text="Sign out", on_click= signout_view)

        page.add(ft.Column([create_project_button]))
        page.add(ft.Column([create_task_button]))
        page.add(ft.Column([add_user_to_project_button]))
        page.add(ft.Column([add_comment_to_task_button]))
        page.add(ft.Column([add_user_to_task_button]))
        page.add(ft.Column([sighn_out_button]))
        # page.add(ft.Column([back_button]))
        page.update()
    
    def go_back(e):
        """Function to navigate back to the main view"""
        main_menu()

    def admin_menu():
        """This function opens admin menu in flet"""
        logger.debug("Opening admin menu")

        page.clean()
        page.add(ft.Text("Welcome Admin!"))

        logger.info("Creating admin menu buttons")
        ban_user_button = ft.ElevatedButton(text="Ban a user", on_click=ban_user_view)
        activate_user_button = ft.ElevatedButton(text="Activate a user", on_click=activate_user_view)
        delete_user_button = ft.ElevatedButton(text="Delete a user", on_click=delete_user_view)

        page.add(ft.Column([ban_user_button]))
        page.add(ft.Column([activate_user_button]))
        page.add(ft.Column([delete_user_button]))
        page.update()

    def ban_user_view(e):
        """opens ban user menu in flet"""
        logger.debug("Opening ban user menu")
        page.clean()
        username = ft.TextField(label="Username you want to ban")
        # ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: ban_user(username.value))

        logger.info("Creating ban user menu button")
        ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: store_ban_result(username.value))
        
        page.add(ft.Column([username, ban_button]))
        page.update()

    def store_ban_result(username):
        """This function takes needed argumant and bans user"""
        # logger.debug(f"attempting to ban user: {username}")
        massage = ban_user(username)

        # logger.info(massage)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def activate_user_view(e):
        """opens activate user menu in flet"""
        logger.debug("Opening activate user menu")
        page.clean()
        username = ft.TextField(label="Username you want to activate")

        logger.info("Adding activate user button")
        activate_button = ft.ElevatedButton(text="Activate", on_click=lambda _: store_activate_result(username.value))

        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_activate_result(username):
        """This function takes needed argumant and activates user"""
        massage = activate_user(username)

        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def delete_user_view(e):
        """opens delet user menu in flet"""
        logger.debug("Opening delet user manu")
        page.clean()
        username = ft.TextField(label="Username you want to delet")
        logger.info("Creating delete user button")
        activate_button = ft.ElevatedButton(text="Delet", on_click=lambda _: store_delet_resualt(username.value))

        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_delet_resualt(username):
        """This function takes needed argumant and delets user"""
        massage = delet_user(username)
        
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def create_project_view(e):
        """opens create project menu in flet"""
        logger.debug("Opening create project menu")

        page.clean()
        project_name = ft.TextField(label="Project Name")
        # logger.info("Create 'crete project' menu button")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        create_button = ft.ElevatedButton(text="Create", on_click=lambda _: create_project(project_name.value))
        
        page.add(ft.Column([back_button,project_name, create_button]))
        # page.add(ft.Column([back_button, create_button]))
        page.update()

    def create_project(project_name):
        """This function takes needed argumant and creates projects. (a username can't have two project with the same name)"""
        logger.debug("Atempting to creat project")
        user = page.session.get("user")

        massage = y.create_project(project_name)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def create_task_view(e):
        """opens create task menu in flet"""
        logger.debug("Opening 'create task' menu")

        page.clean()
        add_task_to_which_project = ft.TextField(label="this task adds to which project?")
        task_name = ft.TextField(label="Task Name")
        task_description = ft.TextField(label="Task Description")
        
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        create_button = ft.ElevatedButton(text="Create", on_click=lambda _: create_task(add_task_to_which_project.value, task_name.value, task_description.value))
        
        page.add(ft.Column([back_button,add_task_to_which_project, task_name, task_description, create_button]))
        page.update()

    def create_task(add_task_to_which_project,task_name, task_description):
        """This function takes needed argumants and creates tasks. (a project can't have two task with the same name)"""
        logger.debug("Atempting to crate a task")

        user = page.session.get("user")
        massage = z.create_task(add_task_to_which_project, task_name, task_description)
        # message = y.create_task(task_name, task_description)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def add_user_to_project_view(e):
        """opens 'add user to project' menu in flet"""
        logger.debug("Opening 'add user to project' menu")

        page.clean()
        username_for_adding_to_project = ft.TextField(label="Username To Add To Project")
        project_name_for_adding_user = ft.TextField(label="Project Name For Adding User To")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        add_button = ft.ElevatedButton(text="Add", on_click=lambda _: add_user_to_project(username_for_adding_to_project.value,project_name_for_adding_user.value))

 
        page.add(ft.Column([back_button,username_for_adding_to_project, project_name_for_adding_user, add_button]))
        page.update()

    def add_user_to_project(uname, pname):
        """This function takes needed argumants and adds user to project."""
        logger.debug("Attemting to add  user to project")
        
        user = page.session.get("user")
        # Add your logic to handle task creation here
        massage = y.add_user_to_project(uname, pname)
        # message = y.create_task(task_name, task_description)
        snackbar.content.value = massage
        print(massage)
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def add_comment_to_task_view(e):
        """opens 'add comment to task' menu in flet"""
        logger.debug("Opening 'add comment to task' menu")

        page.clean()
        pname = ft.TextField(label="This Comment Adds To Which Project?")
        tname = ft.TextField(label="This Comment Adda To Which Task?")
        comment = ft.TextField(label="Your Comment")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        add_comment_button = ft.ElevatedButton(text="Add", on_click=lambda _: add_comment_to_task(pname.value, tname.value, comment.value))

        page.add(ft.Column([back_button,pname, tname, comment, add_comment_button]))
        page.update()

    def add_comment_to_task(pname, tname, comment):
        """This function takes needed argumants and adds comment to task."""
        logger.debug("Attemptin to add comment to task")

        user = page.session.get("user")
        massage = z.add_comment_to_task(pname, tname, comment)

        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def add_user_to_task_view(e):
        """opens 'add task to user' menu in flet"""
        logger.debug("Opening 'add user to task' menu")

        page.clean()
        pname = ft.TextField(label="Project Name Of Task")
        tname = ft.TextField(label="Add User To Which task?")
        uname = ft.TextField(label="Username You Want To Add")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        add_button = ft.ElevatedButton(text="Add", on_click=lambda _: add_user_to_task(pname.value, tname.value, uname.value))
        
        page.add(ft.Column([back_button,pname, tname, uname, add_button]))
        page.update()

    def add_user_to_task(pname, tname, uname):
        """This function takes needed argumants and adds task to user."""
        logger.debug("Attempting to add user to task")

        user = page.session.get("user")
        massage = z.add_user_to_task(pname, tname, uname)

        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def signout_view(e):
        """This function signs out user"""
        logger.debug("Attempting to signout")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        signout_button = ft.ElevatedButton(text="Continue?", on_click=lambda _: signout())

        page.add(ft.Column([back_button,signout_button]))
        page.update()
    
    def signout():
        logger.debug("Attemptong to signout")
        reset_to_main()

    def reset_to_main():
        """This function resets the view history and navigates back to the main function"""
        page.session.set("previous_view", None)
        page.session.set("current_view", None)
        page.session.set("view_history", [])
        main(page)

    # Initial View
    page.add(ft.Column([
        ft.Text("Welcome to Project Management System"),
        ft.ElevatedButton(text="Sign Up", on_click=signup_view),
        ft.ElevatedButton(text="Log In", on_click=login_view),
    ]))
    page.update()

ft.app(target=main)



