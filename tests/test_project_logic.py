import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path
from logic.project_logic import project
from logic.user_logic import UserLogic, get_credentials_from_database_user_id
from model.base_entity import UserEntity

u = UserLogic()
x = project(u)
dic = get_credentials_from_database_user_id()


class TestUserLogic(unittest.TestCase):
    # @patch("logic.user_logic.get_session")  # Adjust the import path as needed
    def test_create_project_existing_project(self):
        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.create_project('a1')
        self.assertEqual(result, "this project name exists")

    def test_add_user_to_project_donot_have_project(self):

        u.login_user('b','b')
        x.user_id = x.use.get_id_user_login()

        result = x.add_user_to_project('new username','dont have project name')
        self.assertEqual(result, "you don't have project with this name!")

    def test_add_user_to_project_usernot_exist(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.add_user_to_project('new username','a1')
        self.assertEqual(result, "The user you want to add to your project does not exist")

    def test_add_user_to_project_useris_in_project(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.add_user_to_project('c','a1')
        self.assertEqual(result, "The user has already been added to your project")        


    def test_list_tasks_project_not_exist(self):
        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.list_tasks("no exist project")
        self.assertEqual(result, False) 

    def test_list_users_project_not_exist(self):
        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.list_users("no exist project")
        self.assertEqual(result, False)   

    def test_delete_project_project_not_exist(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_project("no exist project")
        self.assertEqual(result, "You don't have this project")  

    def test_delete_project_not_leader(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_project("c1")
        self.assertEqual(result, "You are not leader")            

    def test_delete_user_from_project_user_not_exist(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_user_from_project('a1','not exist username')
        self.assertEqual(result, "This username does not exist")

    def test_delete_user_from_project_project_not_exist(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_user_from_project('not exist project','c')
        self.assertEqual(result, "You don't have this project")

    def test_delete_user_from_project_you_arenot_leader(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_user_from_project('c1','b')
        self.assertEqual(result, "You are not leader")

    def test_delete_user_from_project_user_isnot_in_project(self):

        u.login_user('a','a')
        x.user_id = x.use.get_id_user_login()

        result = x.delete_user_from_project('a1','b')
        self.assertEqual(result, "This username isn't in this project")   

        

if __name__ == "__main__":
    unittest.main()
