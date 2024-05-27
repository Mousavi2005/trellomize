import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path
from logic.project_logic import project
from logic.task_logic import Tasks
from logic.user_logic import UserLogic, get_credentials_from_database_user_id
from model.base_entity import UserEntity

u = UserLogic()
x = project(u)
dic = get_credentials_from_database_user_id()



class TestUserLogic(unittest.TestCase):
    # @patch("logic.user_logic.get_session")  # Adjust the import path as needed

    def test_list_users_task_has_no_user(self):
        u.login_user('d','d')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.list_users('d1','dt1')
        self.assertEqual(result, False)

    def test_create_task_project_not_exist(self):
        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.create_task('not exist project', 'a2','task description')
        self.assertEqual(result, "You don't have a project with this name!") 

    def test_create_task_project_has_this_task(self):
        u.login_user('d','d')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.create_task("d1",'dt1','TD')
        self.assertEqual(result, "This project already has this task") 
        
    def test_create_task_not_leader(self):

        u.login_user('c','c')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.create_task("a1",'a2','TD')
        self.assertEqual(result, "You are not the leader of this project") 


    def test_add_comment_to_task_not_in_project(self):
        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.add_comment_to_task('d1', 'dt1' , 'my comment')
        self.assertEqual(result, "You are not in a project with this name!")

    def test_add_comment_to_task_project_desnot_have_this_task(self):
        u.login_user('c','c')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.add_comment_to_task('a1', 'not exist task', 'my comment')
        self.assertEqual(result, "This project doesn't have a task with this name!")

    def test_add_user_to_task_project_not_exist(self):
        u.login_user('d','d')
        x.user_id = x.use.get_id_user_login()
        t = Tasks(x,u)

        result = t.add_user_to_task('not exist peoject', 'dt1', 'c')
        self.assertEqual(result, "You don't have a project with this name!") 


if __name__ == "__main__":
    unittest.main()
