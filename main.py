from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from model.base_entity import Base
from model import base_entity
from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, BigInteger, Boolean, String, ForeignKey, Integer,VARCHAR
from logic.user_logic import UserLogic
from logic.project_logic import project
from logic.task_logic import Tasks
from logic.manager_logic import ban_user, activate_user
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
    page.window_full_screen = True
    page.title = "Project Management System"
    x = UserLogic()
    y = project(x)
    z = Tasks(y,x)

    snackbar = ft.SnackBar(content=ft.Text(""))

    def signup_view(e):
        """Opens signup menu in flet"""
        logger.info("openning signup menu")

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

    def login_view(e):
        """Opens login menu in flet"""
        logger.info("Opening login menu")

        page.clean()
        username = ft.TextField(label="Username")
        password = ft.TextField(label="Password", password=True)
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: reset_to_main(),icon_color=ft.colors.RED)
        login_button = ft.ElevatedButton(content=ft.Text("Login",size=20), on_click=lambda _: login(username.value, password.value),width=120, height=40)
        page.add(ft.Column([back_button, username, password, login_button]))
        page.update()

    def login(username: str, password: str) -> None:
        """This function takes needed arguments and connects user to database (if user diesnt have account they have to signup first)"""
        logger.debug(f"Attempting to login user: {username}")

        if x.login_user(username, password) == "Admin":
            snackbar.content.value = "login successful admin"
            admin_menu()
        elif x.login_user(username, password) == True:
            page.session.set("user", username)
            snackbar.content.value = "login successful!"
            main_menu()
        elif x.login_user(username, password) == "NA":
            snackbar.content.value = "Unfortunetly you are baned. please contact adminastrator"
        else:
            snackbar.content.value = "Invalid credentials"
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()

    def main_menu():
        """This function opens the main menu in flet"""
        logger.info("Opening main menu")

        page.clean()
        user = page.session.get("user")
        if user:
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
        logger.info("Opening 'admin' menu")

        page.clean()
        text = ft.Text("Welcome Admin!", size=40)
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: reset_to_main(),icon_color=ft.colors.RED)
        ban_user_button = ft.ElevatedButton(content=ft.Text("Ban a user", size= 35), on_click=ban_user_view,width=340, height=150, color= ft.colors.RED)
        activate_user_button = ft.ElevatedButton(content=ft.Text("Activate a user", size= 35), on_click=activate_user_view,width=340, height=150, color= ft.colors.GREEN)

        row = ft.Row(
        [
            ban_user_button,    
            activate_user_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )

        row2 = ft.Row(
        [
            back_button,    
            text,
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 550
        )

        resualt = ft.Column(
        [
            row2,    
            row,
        ], 
        spacing= 150
        )

        page.add(resualt)
        page.update()

    def ban_user_view(e):
        """This function opens 'ban user' menu"""
        logger.info("Opening 'ban user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to ban")
        ban_button = ft.ElevatedButton(text="Ban", on_click=lambda _: store_ban_result(username.value))
        page.add(ft.Column([username, ban_button]))
        page.update()

    def store_ban_result(username: str) -> None:
        """This function takes needed argumant and bans user"""
        logger.debug(f"attempting to ban user: {username}")

        massage = ban_user(username)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def activate_user_view(e):
        """opens activate user menu in flet"""
        logger.info("Opening 'activate user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to activate")
        activate_button = ft.ElevatedButton(text="Activate", on_click=lambda _: store_activate_result(username.value))
        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_activate_result(username: str) -> None:
        """This function takes needed argumant and activates user"""
        logger.debug(f"Atemting to activate user : {username}")
        
        massage = activate_user(username)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def delete_user_view(e):
        """This function opens delet user menu in flet"""
        logger.info("Opening 'delete user' menu")

        page.clean()
        username = ft.TextField(label="Username you want to delet")
        activate_button = ft.ElevatedButton(text="Delet", on_click=lambda _: store_delet_resualt(username.value))
        page.add(ft.Column([username, activate_button]))
        page.update()

    def store_delet_resualt(username: str) -> None:
        """This function takes needed argumant and delets user"""
        logger.debug(f"Atempting to delete user : {username}")

        massage = delet_user(username)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        admin_menu()
        page.update()

    def create_project_view(e):
        """opens 'create project' menu in flet"""
        logger.info("Opening 'project' menu")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        create_button = ft.ElevatedButton(content=ft.Text("Create project",size=35), on_click=create_project_view2,width=340, height=150, color= ft.colors.BLUE)
        task_list_button = ft.ElevatedButton(content=ft.Text("Task list",size=35), on_click=task_list_view,width=340, height=150, color= ft.colors.BLUE)
        user_list_button = ft.ElevatedButton(content=ft.Text("user list", size=35), on_click=user_list_view, width=340, height=150, color=ft.colors.BLUE)
        delete_project_button = ft.ElevatedButton(content=ft.Text("Delete project", size=35), on_click=delete_project_view, width=340, height=150, color=ft.colors.BLUE)
        delete_user_from_project_button = ft.ElevatedButton(content=ft.Text("Delete user", size=35), on_click=delete_user_from_project_view, width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [
            create_button,    
            task_list_button,
            user_list_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )

        row2 = ft.Row(
            [
                # leader_project_list_button,
                delete_project_button,
                delete_user_from_project_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=150
        )
        resualt = ft.Column(
        [
            ft.Row([back_button]),
            row,
            row2
        ],
        spacing=150
        )

        page.add(resualt)
        page.update()

    def leader_project_list_view(e):

        logger.debug("Attempting to show 'project list' in 'project' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=user_view,icon_color=ft.colors.RED)
        text = ft.Text("Projects you are leader in", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = x.list_leader_project()

        if massage == False:
            
            snackbar.content.value = "You don't have this project"
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

    def delete_project_view(e):
        """opens 'delete project' menu in flet"""
        logger.info("Opening 'delete project' menu")

        page.clean()
        project_name = ft.TextField(label="Project Name")

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        create_button = ft.ElevatedButton(content=ft.Text("Delete",size=20), on_click=lambda _: delete_project(e, project_name.value),width=130, height=40)

        page.add(ft.Column([back_button, project_name, create_button]))
        page.update()

    def delete_project(e, pname):
        """This function takes needed arguments and deletes a project"""
        logger.debug(f"Atempting to delete {pname} project")

        massage = y.delete_project(pname)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        create_project_view(e)

        page.update()

    def delete_user_from_project_view(e):
        """This function opens 'delet user from project' menu"""
        logger.info("Opening 'delete user' menu")

        page.clean()
        project_name = ft.TextField(label="Project Name")
        user_name = ft.TextField(label="user Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        delete_button = ft.ElevatedButton(content=ft.Text("Delete",size=20), on_click=lambda _: delete_user_from_project(e, project_name.value, user_name.value),width=130, height=40)
        page.add(ft.Column([back_button, project_name, user_name, delete_button]))
        page.update()

    def delete_user_from_project(e, pname, uname):
        """This function takes needed arguments and deletes a user from a project"""
        logger.debug(f"Atempting to delete user : {uname}, from project : {pname}")

        massage = y.delete_user_from_project(pname, uname)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        create_project_view(e)
        page.update()

    def create_project_view2(e):
        """This function opens 'create project' menu"""
        logger.info("Opening 'create project' menu")

        page.clean()
        project_name = ft.TextField(label="Project Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        create_button = ft.ElevatedButton(content=ft.Text("Create",size=20), on_click=lambda _: create_project(e, project_name.value),width=130, height=40)
        page.add(ft.Column([back_button, project_name, create_button]))
        page.update()

    def task_list_view(e):
        """This function opens 'task list' menu"""
        logger.info("Oppening 'task list' in 'project' menu")
        
        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="Project name ?")
        create_button = ft.ElevatedButton(content=ft.Text("List",size=20), on_click=lambda _: list_task(e, pname.value) ,width=130, height=40)
        page.add(ft.Column([back_button, pname, create_button]))
        page.update()

    def user_view(e):
        """opens 'User' menu"""
        logger.debug("Oppening 'User' menu")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back, icon_color=ft.colors.RED)
        leader_project_list_button = ft.ElevatedButton(content=ft.Text("Leader Projects", size=35), on_click=leader_project_list_view, width=340, height=150, color=ft.colors.BLUE)
        pl_button = ft.ElevatedButton(content=ft.Text("Show projects",size=35), on_click=lambda _: list_project2() ,width=340, height=150, color=ft.colors.BLUE)
        tl_button = ft.ElevatedButton(content=ft.Text("Show tasks",size=35), on_click=lambda _: list_task2() ,width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [ 
            leader_project_list_button,
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

    def user_list_view(e):
        logger.debug("Attempting to open 'userlist' in 'project'")
        
        page.clean()
        # project_name = ft.TextField(label="Project Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="Project name ")

        create_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: project_user_list(e, pname.value) ,width=140, height=30)

        page.add(ft.Column([back_button, pname, create_button]))
        page.update()

    def project_user_list(e, pname):
        
        logger.debug("Attempting to show 'users list' in 'project' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
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
            
            snackbar.content.value = "You don't have this project"
            snackbar.open = True
            page.snack_bar = snackbar
            create_project_view(e)

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

    def create_project(e, project_name: str) -> None:
        """This function takes needed argumant and creates projects. (a username can't have two project with the same name)"""
        logger.debug(f"Atempting to creat {project_name} project")

        user = page.session.get("user")

        massage = y.create_project(project_name)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        create_project_view(e)
        page.update()

    def list_project2():
        logger.debug("Attempting to show 'project list' in 'User'")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=user_view,icon_color=ft.colors.RED)
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
        logger.info("Opening 'Task' menu")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        create_button = ft.ElevatedButton(content=ft.Text("Create task",size=35), on_click=create_task_view2,width=340, height=150, color= ft.colors.BLUE)
        edit_task_button = ft.ElevatedButton(content=ft.Text("Edit task",size=35), on_click=edit_task_view,width=340, height=150, color= ft.colors.BLUE)
        delete_user_button = ft.ElevatedButton(content=ft.Text("Delete user",size=35), on_click=delete_user_task_view,width=340, height=150, color= ft.colors.BLUE)

        history_button = ft.ElevatedButton(content=ft.Text("History",size=35), on_click=history_view,width=340, height=150, color= ft.colors.BLUE)
        task_list_button = ft.ElevatedButton(content=ft.Text("Comment list",size=35), on_click=comment_list_view,width=340, height=150, color= ft.colors.BLUE)
        user_list_button = ft.ElevatedButton(content=ft.Text("Users list", size=35), on_click= user_list_view2, width=340, height=150, color=ft.colors.BLUE)

        row = ft.Row(
        [
            create_button,
            edit_task_button,
            delete_user_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )
        
        row2 = ft.Row(
        [
            user_list_button,
            task_list_button,
            history_button
        ],
        alignment=ft.MainAxisAlignment.CENTER , 
        spacing= 150
        )

        resualt = ft.Column(
        [
            ft.Row([back_button]),
            row,
            row2
        ],
        spacing=150
        )

        page.add(resualt)
        page.update()

    def user_list_view2(e):
        """opens 'user list' menu in 'Task"""
        logger.debug("Oppening 'user list' menu in 'Task'")

        page.clean()
        pname = ft.TextField(label="Project Name")
        tname = ft.TextField(label="Task Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        list_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: list_user2(e, pname.value, tname.value) ,width=130, height=40)
        page.add(ft.Column([back_button,pname,tname, list_button]))
        page.update()

    def list_user2(e, pname: str, tname: str) -> None:

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
            create_task_view(e)

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

    def comment_list_view(e):
        """opens 'comments list' in flet"""
        logger.info("openning 'comment list' menu")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="project name")
        tname = ft.TextField(label="task name")
        create_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: list_comment1(pname.value, tname.value) ,width=130, height=40)
        page.add(ft.Column([back_button, pname, tname, create_button]))
        page.update()

    def list_comment1(pname: str, tname: str) -> None:
        """This function shows list of comments in a task"""
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
        """opens 'create task' menu in flet"""
        logger.info("Oppening 'create task' menu")
        
        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        add_task_to_which_project = ft.TextField(label="Project Name")
        task_name = ft.TextField(label="Task Name")
        priority = ft.TextField(label="Priority")
        status = ft.TextField(label="Status")
        task_description = ft.TextField(label="Task Description")
        # start_date = ft.TextField(label="Start date")
        finish_date = ft.TextField(label="Finish date")
        create_button = ft.ElevatedButton(content=ft.Text("Create",size=20), on_click=lambda _: create_task(add_task_to_which_project.value, task_name.value, task_description.value, priority.value, status.value, finish_date.value),width=130, height=40)
        page.add(ft.Column([back_button, add_task_to_which_project, task_name,priority, status , task_description, finish_date, create_button]))
        page.update()

    def edit_task_view(e):
        """opens 'edit task' menu in flet"""
        logger.info("Openning 'edit task' menu")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="Project Name")
        tname = ft.TextField(label="Task Name")
        priority = ft.TextField(label="Priority")
        status = ft.TextField(label="Status")
        description = ft.TextField(label="Description")
        edit_button = ft.ElevatedButton(content=ft.Text("Edit",size=20), on_click=lambda _: edit_task(pname.value, tname.value, priority.value, status.value, description.value),width=130, height=40)
        page.add(ft.Column([back_button, pname, tname, priority, status, description, edit_button]))
        page.update()

    def delete_user_task_view(e):
        """opens 'delete user' menu in 'task'"""
        logger.info("Openning 'delete user' menu in 'task'")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        pname = ft.TextField(label="Project Name")
        tname = ft.TextField(label="Task Name")
        uname = ft.TextField(label="Username")
        delete_button = ft.ElevatedButton(content=ft.Text("Edit",size=20), on_click=lambda _: delete_user_task(e ,pname.value, tname.value, uname.value),width=130, height=40)
        page.add(ft.Column([back_button, pname, tname, uname, delete_button]))
    
    def delete_user_task(e, pname, tname, uname):
        """This function takes needed arguments and deletes a user from project"""
        logger.debug(f"Atempting to delete username : {uname} from task : {tname}")

        massage = z.delete_user_from_task(pname, tname, uname)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        create_project_view(e)

        page.update()

    def history_view(e):
        """opens 'task history' menu in flet """
        logger.debug("Oppening 'task history' menu")

        page.clean()
        pname = ft.TextField(label="Project Name")
        tname = ft.TextField(label="Task Name")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        show_button = ft.ElevatedButton(content=ft.Text("Show",size=20), on_click=lambda _: show_history(e, pname.value, tname.value) ,width=130, height=40)
        page.add(ft.Column([back_button,pname,tname, show_button]))
        page.update()

    def show_history(e, pname, tname):
        logger.debug("Attempting to show 'task history' ")
        page.clean()

        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_task_view,icon_color=ft.colors.RED)
        text = ft.Text("History of this task", size=45)
        
        row = ft.Row(
        [
            back_button,    
            text,
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 530
        )
        page.add(row)

        massage = z.list_history(pname, tname)

        if massage == "you dont have a project with this name":
            
            snackbar.content.value = "you dont have a project with this name"
            snackbar.open = True
            page.snack_bar = snackbar
            create_task_view(e)

        elif massage == "this task dose not exist in this project":
            
            snackbar.content.value = "this task dose not exist in this project"
            snackbar.open = True
            page.snack_bar = snackbar
            create_task_view(e)       

        elif massage == "you not member in this project!":
            
            snackbar.content.value = "you not member in this project!"
            snackbar.open = True
            page.snack_bar = snackbar
            create_task_view(e)   

        else:
            # snackbar.content.value = massage
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for h in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{h}", size=35))
                page.update()
            
            sleep(1)

        page.update()

    def edit_task(pname, tname, priority, status, description):
        """This function takes needed argumants and creates tasks. (a project can't have two task with the same name)"""
        logger.debug(f"Atempting to edit {tname} task")

        number = z.edit_task(pname, tname, priority, status, description)
        massage = ''
        if number == 0 :
            massage = "Task edited"
        elif number == 5 :
            massage = "invalid status"
        elif number == 10 :
            massage = "invalid priority"
        elif number == 15 :
            massage = "invalid priority and status"
           
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def list_task(e, pname: str) -> None:
        """This function shows 'task list' in 'project'"""
        logger.debug("Attempting to show 'tasks list' in 'project' ")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=create_project_view,icon_color=ft.colors.RED)
        text = ft.Text("Tasks in this project", size=45)
        row = ft.Row(
        [
            back_button,    
            text,
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
            create_project_view(e)
        else:
            lv = ft.ListView(expand=1, spacing=10, padding=20,)
            page.add(lv)

            for task in massage :
                sleep(1)
                lv.controls.append(ft.Text(f"{task}", size=35))
                page.update()
            
            sleep(1)
        page.update()

    def list_task2():
        """This function shows 'task list' in 'user' """
        logger.debug("Attempting to show 'tasks list' in 'User' ")

        page.clean()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=user_view,icon_color=ft.colors.RED)
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
        page.update()

    def create_task(add_task_to_which_project: str,task_name: str, task_description: str, priority, status, finish_date) -> None:
        """This function takes needed argumants and creates tasks. (a project can't have two task with the same name)"""
        logger.debug(f"Atempting to crate {task_name} task")
        # user = page.session.get("user")
        massage = z.create_task(add_task_to_which_project, task_name, task_description, priority, status, finish_date)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def add_user_to_project_view(e):
        """opens 'add user to project' menu in flet"""
        logger.info("Opening 'add user to project' menu")

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
        # user = page.session.get("user")
        massage = y.add_user_to_project(uname, pname)
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
        # user = page.session.get("user")
        massage = z.add_comment_to_task(pname, tname, comment)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def add_user_to_task_view(e):
        """opens 'add task to user' menu in flet"""
        logger.info("Opening 'add user to task' menu")

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
        # user = page.session.get("user")
        massage = z.add_user_to_task(pname, tname, uname)
        snackbar.content.value = massage
        snackbar.open = True
        page.snack_bar = snackbar
        main_menu()
        page.update()

    def signout_view(e):
        """This function signs out user"""
        logger.info("Oppening 'signout' menu")

        page.clean()
        left_text = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back,icon_color=ft.colors.RED)
        center_container = ft.Text("Do you want to signout?", size=35)
        row = ft.Row(
        [
            left_text,
            center_container 
        ],
        alignment=ft.MainAxisAlignment.START ,
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
        """This function signs out user"""
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
        """This function close flet window"""
        logger.info("Attempting to exit the app")
        page.window_close()
    
    left_text = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=close_window,icon_color=ft.colors.RED)
    center_container = ft.Text("Welcome to Project Management System", size=35)
    row = ft.Row(
        [
            left_text,    
            center_container  
        ],
        alignment=ft.MainAxisAlignment.START , 
        spacing= 420
    )

    row2 = ft.Row([

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



