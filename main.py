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
from time import sleep


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
    """Flet function to open a page"""
    logger.info("Openning main page")

    page.clean()

    # page.window_height = 400
    # page.window_width = 900
    page.window_full_screen = True
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

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: reset_to_main(), icon_color=ft.colors.RED)
        signup_button = ft.ElevatedButton(content=ft.Text("Sign up",size=20), on_click=lambda _: signup(username.value, gmail.value, password.value), width=130, height=40)

        page.add(ft.Column([back_button, username, gmail, password, signup_button]))
        page.update()

    def signup(username: str, gmail: str, password: str) -> None:
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

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: reset_to_main(),icon_color=ft.colors.RED)
        login_button = ft.ElevatedButton(content=ft.Text("Login",size=20), on_click=lambda _: login(username.value, password.value),width=120, height=40)

        page.add(ft.Column([back_button, username, password, login_button]))
        page.update()
        # print(x.get_id_user_login())

    def login(username: str, password: str) -> None:
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
            # page.add(ft.Text(f"Welcome {user}!"))
            # page.add(ft.Row([ft.Text(f"Welcome {user}!", size=35)],alignment='center'))
            page.add(
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            f"Welcome {user}!",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    gradient=ft.PaintLinearGradient(
                                        (0, 20), (150, 20), [ft.colors.RED, ft.colors.YELLOW]
                                    )
                                ),
                            ),
                        ),
                    ],
                )
            )


        else:
            page.add(ft.Text("Welcome!"))

        create_project_button = ft.ElevatedButton(content=ft.Text("project",size=35),on_click=create_project_view, width=340,height=150, color= ft.colors.BLUE)
        create_task_button = ft.ElevatedButton(content=ft.Text("Task",size=35),on_click=create_task_view, width=340,height=150, color= ft.colors.BLUE)
        user_button = ft.ElevatedButton(content=ft.Text("User",size=35),on_click=user_view, width=340,height=150, color= ft.colors.BLUE)


        add_user_to_project_button = ft.ElevatedButton(content=ft.Text("Add User To Project",size=30),on_click=add_user_to_project_view, width=340,height=150, color=ft.colors.GREEN)
        add_comment_to_task_button = ft.ElevatedButton(content=ft.Text("Add Comment To Task",size=30),on_click=add_comment_to_task_view, width=370,height=150, color=ft.colors.GREEN)
        add_user_to_task_button = ft.ElevatedButton(content=ft.Text("Add User To Task",size=30), on_click=add_user_to_task_view, width=340,height=150, color=ft.colors.GREEN)

        sighn_out_button = ft.ElevatedButton(content=ft.Text("sign out",size=35), on_click= signout_view, width=340,height=150, color=ft.colors.RED)

        page.add(ft.Row([create_project_button, create_task_button, user_button],alignment="center"))
        page.add(ft.Row([add_user_to_project_button, add_comment_to_task_button, add_user_to_task_button],alignment="center"))
        page.add(ft.Row([sighn_out_button],alignment="center"))
        page.update()
    
    def go_back(e):
        """Function to navigate back to the main view"""
        logger.debug("Attempting to go to main menu")
        main_menu()

    def admin_menu():
        """This function opens admin menu in flet"""
        logger.debug("Opening 'admin' menu")

        page.clean()
        page.add(ft.Text("Welcome Admin!"))

        ban_user_button = ft.ElevatedButton(text="Ban a user", on_click=ban_user_view)
        activate_user_button = ft.ElevatedButton(text="Activate a user", on_click=activate_user_view)
        delete_user_button = ft.ElevatedButton(text="Delete a user", on_click=delete_user_view)

        page.add(ft.Column([ban_user_button]))
        page.add(ft.Column([activate_user_button]))
        page.add(ft.Column([delete_user_button]))
        page.update()

    def ban_user_view(e):
        """opens ban user menu in flet"""
        logger.debug("Opening 'ban user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to ban")

        ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: store_ban_result(username.value))
        
        page.add(ft.Column([username, ban_button]))
        page.update()

    def store_ban_result(username: str) -> None:
        """This function takes needed argumant and bans user"""
        logger.debug(f"attempting to ban user: {username}")

        massage = ban_user(username)

        # logger.info(massage)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def activate_user_view(e):
        """opens activate user menu in flet"""
        logger.debug("Opening 'activate user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to activate")

        activate_button = ft.ElevatedButton(text="Activate", on_click=lambda _: store_activate_result(username.value))

        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_activate_result(username: str) -> None:
        """This function takes needed argumant and activates user"""
        logger.debug(f"Atemting to activate {username}")

        
        massage = activate_user(username)

        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def delete_user_view(e):
        """opens delet user menu in flet"""
        logger.debug("Opening 'delet user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to delet")

        activate_button = ft.ElevatedButton(text="Delet", on_click=lambda _: store_delet_resualt(username.value))

        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_delet_resualt(username: str) -> None:
        """This function takes needed argumant and delets user"""
        logger.debug(f"Atempting to delete {username}")

        massage = delet_user(username)
        
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def create_project_view(e):
        """opens create project menu in flet"""
        logger.debug("Opening 'project' menu")

        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)

        create_button = ft.ElevatedButton(content=ft.Text("Create project",size=35), on_click=create_project_view2,width=340, height=150, color= ft.colors.BLUE)
        task_list_button = ft.ElevatedButton(content=ft.Text("Task list",size=35), on_click=task_list_view,width=340, height=150, color= ft.colors.BLUE)
        user_list_button = ft.ElevatedButton(content=ft.Text("user list", size=35), on_click=user_list_view, width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [
            create_button,    
            task_list_button,
            user_list_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )
        resualt = ft.Column(
        [
            ft.Row([back_button]),
            row
        ],
        spacing=250
        )

        page.add(resualt)
        page.update()

    def create_project_view2(e):

        logger.debug("Opening 'create project' menu")

        page.clean()
        project_name = ft.TextField(label="Project Name")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        create_button = ft.ElevatedButton(content=ft.Text("Create",size=20), on_click=lambda _: create_project(project_name.value),width=130, height=40)

        page.add(ft.Column([back_button, project_name, create_button]))
        page.update()

    def task_list_view(e):
        logger.debug("Oppening 'task list' in 'project' menu")
        page.clean()
        # project_name = ft.TextField(label="Project Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)

        pname = ft.TextField(label="Project name ?")
        create_button = ft.ElevatedButton(content=ft.Text("List",size=20), on_click=lambda _: list_task(pname.value) ,width=130, height=40)

        page.add(ft.Column([back_button, pname, create_button]))
        page.update()

    def user_view(e):
        logger.debug("Oppening 'User' menu")

        page.clean()
        # project_name = ft.TextField(label="Project Name")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back, icon_color=ft.colors.RED)
        pl_button = ft.ElevatedButton(content=ft.Text("Show projects",size=35), on_click=lambda _: list_project2() ,width=340, height=150, color=ft.colors.BLUE)
        tl_button = ft.ElevatedButton(content=ft.Text("Show tasks",size=35), on_click=lambda _: list_task2() ,width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [ 
            pl_button,
            tl_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )
        resualt = ft.Column(
        [
            ft.Row([back_button]),
            row
        ],
        spacing=250
        )

        page.add(resualt)
        page.update()

    # def list_task1():
        
    #     # logger.debug("Atempting to creat project")
    #     user = page.session.get("user")

    #     snackbar.content.value = "task list for project part"
    #     snackbar.open = True
    #     page.snack_bar = snackbar
    #     main_menu()
    #     page.update()

    # def list_task2():
        
    #     logger.debug("Atempting to show 'task list' in 'users' ")

    #     user = page.session.get("user")

    #     snackbar.content.value = "task list for user part"
    #     snackbar.open = True
    #     page.snack_bar = snackbar
    #     main_menu()
    #     page.update()

    def user_list_view(e):
        logger.debug("Attempting to open 'userlist' in 'project'")
        
        page.clean()
        # project_name = ft.TextField(label="Project Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="Project name ")

        create_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: project_user_list(pname.value) ,width=140, height=30)

        page.add(ft.Column([back_button, pname, create_button]))
        page.update()

    def project_user_list(pname):
        
        logger.debug("Attempting to show 'users list' in 'project' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("users in this project", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
            # user_list_button
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = y.list_users(pname)

        if massage == False:
            
            snackbar.content.value = "You don't have this project or you don't have this task in project"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()

        else:
            # snackbar.content.value = massage
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for task in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{task}", size=35))
                page.update()
            
            sleep(1)

        page.update()


    def list_user1():
        
        logger.debug("Atempting to list users of a project")
        user = page.session.get("user")

        snackbar.content.value = "user list for project part"
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def create_project(project_name: str) -> None:
        """This function takes needed argumant and creates projects. (a username can't have two project with the same name)"""
        logger.debug(f"Atempting to creat {project_name} project")

        user = page.session.get("user")

        massage = y.create_project(project_name)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    # def list_project_view(e):
    #     page.clean()
    #     list_button = ft.ElevatedButton(content=ft.Text("List",size=20), on_click=lambda _: list_project(),width=340, height=150)

    #     page.add(ft.Column([list_button]))
    #     page.update()

    # def list_project():
        
    #     snackbar.content.value = "Passed"
    #     snackbar.open = True
    #     page.snack_bar = snackbar
    #     # go_back(e)
    #     main_menu()
        
    #     page.update()
    #     # pass

    def list_project2():
        logger.debug("Attempting to show 'project list' in 'User'")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("You are in these projects", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
            # user_list_button
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 450
        )
        page.add(row)

        dic = x.list_projects()

        if dic == False:
        
            snackbar.content.value = "You are not in any project yet"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()
        else:

            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for p in dic :
                sleep(1)
                lv.controls.append(ft.Text(f"{p}",size=35))
                page.update()
            sleep(1)

        page.update()

    def create_task_view(e):
        """opens create task menu in flet"""
        logger.debug("Opening 'Task' menu")

        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)

        create_button = ft.ElevatedButton(content=ft.Text("Create task",size=35), on_click=create_task_view2,width=340, height=150, color= ft.colors.BLUE)
        task_list_button = ft.ElevatedButton(content=ft.Text("Comment list",size=35), on_click=comment_list_view,width=340, height=150, color= ft.colors.BLUE)
        user_list_button = ft.ElevatedButton(content=ft.Text("Users list", size=35), on_click= user_list_view2, width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [
            create_button,    
            task_list_button,
            user_list_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )
        resualt = ft.Column(
        [
            ft.Row([back_button]),
            row
        ],
        spacing=250
        )

        page.add(resualt)
        page.update()

    def user_list_view2(e):
        logger.debug("Oppening 'user list' menu in 'Task'")

        page.clean()
        pname = ft.TextField(label="Project Name")
        tname = ft.TextField(label="Task Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        list_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: list_user2(pname.value, tname.value) ,width=130, height=40)

        page.add(ft.Column([back_button,pname,tname, list_button]))
        page.update()

    def list_user2(pname, tname):

        logger.debug("Attempting to show 'users list' in 'Task' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("Users in this Task", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
            # user_list_button
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = z.list_users(pname, tname)

        if massage == False:
            
            snackbar.content.value = "This task doesn't have any user"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()

        else:
            # snackbar.content.value = massage
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for task in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{task}", size=35))
                page.update()
            
            sleep(1)

        # snackbar.content.value = "1"
        # snackbar.open = True
        # page.snack_bar = snackbar
        # go_back(e)
        # main_menu()
        page.update()

    def comment_list_view(e):
        page.clean()
        # project_name = ft.TextField(label="Project Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="project name")
        tname = ft.TextField(label="task name")
        create_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: list_comment1(pname.value, tname.value) ,width=130, height=40)

        page.add(ft.Column([back_button, pname, tname, create_button]))
        page.update()

    def list_comment1(pname, tname):

        logger.debug("Attempting to show 'comments list' in 'Task' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("comments in this Task", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = z.list_comment(pname, tname)

        if massage == False:
            
            snackbar.content.value = "This task doesn't have any comments"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()

        else:
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for task in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{task}", size=35))
                page.update()
            
            sleep(1)

        page.update()

    def create_task_view2(e):
        logger.debug("Oppening 'create task' menu")
        
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        add_task_to_which_project = ft.TextField(label="this task adds to which project?")
        task_name = ft.TextField(label="Task Name")
        task_description = ft.TextField(label="Task Description")

        create_button = ft.ElevatedButton(content=ft.Text("Create",size=20), on_click=lambda _: create_task(add_task_to_which_project.value, task_name.value, task_description.value),width=130, height=40)
                
        page.add(ft.Column([back_button, add_task_to_which_project, task_name, task_description,create_button]))
        page.update()

    # def list_task_view(e):

    #     page.clean()

    #     # pname = ft.TextField(label="Project name ?")
    #     list_button = ft.ElevatedButton(content=ft.Text("List",size=20), on_click=lambda _: list_task(pname.value),width=340, height=150)

    #     page.add(ft.Column([list_button]))
    #     page.update()

    def list_task(pname):
        # snackbar.content.value = "Passed"
        logger.debug("Attempting to show 'tasks list' in 'project' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("Tasks in this project", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
            # user_list_button
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = y.list_tasks(pname)

        if massage == False:
            
            snackbar.content.value = "You don't have this project or you don't have this task in project"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()

        else:
            # snackbar.content.value = massage
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for task in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{task}", size=35))
                page.update()
            
            sleep(1)

        page.update()

    def list_task2():
        logger.debug("Attempting to show 'tasks list' in 'User' ")

        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        text = ft.Text("You are in these tasks", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
            # user_list_button
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        dic = x.list_tasks()
        if dic == False: 

            snackbar.content.value = "You are not in any task yet"
            snackbar.open = True
            page.snack_bar = snackbar
            main_menu()
        else:

            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for t in dic :
                sleep(1)
                lv.controls.append(ft.Text(f"{t}",size=35))
                page.update()
            sleep(1)

        # snackbar.content.value = "list task for user part"
        # snackbar.open = True
        # page.snack_bar = snackbar
        
        # main_menu()
        page.update()

    def create_task(add_task_to_which_project: str,task_name: str, task_description: str) -> None:
        """This function takes needed argumants and creates tasks. (a project can't have two task with the same name)"""
        logger.debug(f"Atempting to crate {task_name} task")

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

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        add_button = ft.ElevatedButton(content=ft.Text("Add",size=20), on_click=lambda _: add_user_to_project(username_for_adding_to_project.value,project_name_for_adding_user.value),width=120, height=40)

 
        page.add(ft.Column([back_button,username_for_adding_to_project, project_name_for_adding_user, add_button]))
        page.update()

    def add_user_to_project(uname: str, pname: str) -> None:
        """This function takes needed argumants and adds user to project."""
        logger.debug(f"Attemting to add {uname} user to {pname} project")
        
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

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        add_comment_button = ft.ElevatedButton(content=ft.Text("Add",size=20), on_click=lambda _: add_comment_to_task(pname.value, tname.value, comment.value),width=120, height=40)

        page.add(ft.Column([back_button,pname, tname, comment, add_comment_button]))
        page.update()

    def add_comment_to_task(pname: str, tname: str, comment: str) -> None:
        """This function takes needed argumants and adds comment to task."""
        logger.debug(f"Attemptin to add {comment} comment to {tname} task")

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

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        add_button = ft.ElevatedButton(content=ft.Text("Add",size=20), on_click=lambda _: add_user_to_task(pname.value, tname.value, uname.value),width=120, height=40)
        
        page.add(ft.Column([back_button,pname, tname, uname, add_button]))
        page.update()

    def add_user_to_task(pname: str, tname: str, uname: str) -> None:
        """This function takes needed argumants and adds task to user."""
        logger.debug(f"Attempting to add {uname} user to {tname} task")

        user = page.session.get("user")
        massage = z.add_user_to_task(pname, tname, uname)

        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def signout_view(e):
        """This function signs out user"""
        logger.debug("Oppening 'signout' menu")
        page.clean()

        # back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back)
        left_text = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        center_container = ft.Text("Do you want to signout?", size=35)

        row = ft.Row(
        [
            left_text,     # Left-aligned text
            center_container  # Center-aligned text within its container
        ],
        alignment=ft.MainAxisAlignment.START , # Align items in the row to the start (left)
        spacing= 520
        ) 
        signout_button = ft.Row([ft.ElevatedButton(content=ft.Text("Continue",size=30), on_click=lambda _: signout(),width=340, height=150, color=ft.colors.RED)], alignment='center')

        resualt = ft.Column(
            [
                row,
                signout_button
            ],
            spacing=200,
        )
        page.add(resualt)
        page.update()
    
    def signout():
        logger.debug("Attemptong to signout")

        snackbar.content.value = "Signout successfully"
        snackbar.open = True
        page.snack_bar = snackbar

        reset_to_main()

    def reset_to_main():
        """This function resets the view history and navigates back to the main function"""
        page.session.set("previous_view", None)
        page.session.set("current_view", None)
        page.session.set("view_history", [])
        main(page)

    def close_window(e):
        logger.debug("Attempting to exit the app")
        page.window_close()
    
    
    
    
    # Initial View
    # page.add(ft.Row([ft.Text("Welcome to Project Management System")], alignment='center'))
    # page.add(ft.Row([ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=close_window)]))
    left_text = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=close_window,icon_color=ft.colors.RED)
    center_container = ft.Text("Welcome to Project Management System", size=35)
    row = ft.Row(
        [
            left_text,     # Left-aligned text
            center_container  # Center-aligned text within its container
        ],
        alignment=ft.MainAxisAlignment.START , # Align items in the row to the start (left)
        spacing= 420
    )
    # page.add(row)
    row2 = ft.Row([
        # ft.Text("Welcome to Project Management System"),
        # ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=close_window),
        ft.ElevatedButton(content=ft.Text("Sign up",size=40), on_click=signup_view, width=340,height=150, color= ft.colors.BLUE),
        ft.ElevatedButton(content=ft.Text("Login",size=40), on_click=login_view, width=340,height=150, color= ft.colors.BLUE),
    ], alignment='center',spacing=200)

    resualt = ft.Column(
        [
            row,
            row2
        ],
        spacing=300
    )
    page.add(resualt)

    page.update()

ft.app(target=main)



