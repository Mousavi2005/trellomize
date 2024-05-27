import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path
from logic.user_logic import UserLogic
from model.base_entity import UserEntity

x = UserLogic()

class TestUserLogic(unittest.TestCase):
    # @patch("logic.user_logic.get_session")  # Adjust the import path as needed
    def test_signup_used_username(self):  # Renamed the test method to start with 'test_'
        result = x.signup_user('a', 'unusedgmail@gmail.com','a')
        self.assertEqual(result, False)

    def test_signup_used_gmail(self):
        resualt = x.signup_user('new user', 'a@gmail.com','new user')
        self.assertEqual(resualt,"UG")

    def test_signup_not_valid_gmail(self):
        resualt = x.signup_user('new user', '#newuser@gmail.com','new password')
        self.assertEqual(resualt,"NVG")

    def test_login_user_user_isnot_in_database(self):
        resualt = x.login_user('not in database','not in database')
        self.assertEqual(resualt,False)

    def test_login_user_user_is_admin(self):
        resualt = x.login_user('admin','007')
        self.assertEqual(resualt,'Admin')

    def test_login_user_not_active(self):
        resualt = x.login_user('b','b')
        self.assertEqual(resualt,'NA')

    def test_login_user_correct(self):
        resualt = x.login_user('a','a')
        self.assertEqual(resualt,True)

    def test_list_projects_user_isnot_in_anyproject(self):
        existing_user = x.session.query(UserEntity).filter(UserEntity.username == "b").first()
        x.id = existing_user.id

        resualt = x.list_projects()
        self.assertEqual(resualt,False)

    def test_list_task_user_isnot_in_any_task(self):
        existing_user = x.session.query(UserEntity).filter(UserEntity.username == "b").first()
        x.id = existing_user.id

        resualt = x.list_projects()
        self.assertEqual(resualt,False)

    def test_list_leader_project_user_isnot_leader(self):
        existing_user = x.session.query(UserEntity).filter(UserEntity.username == "b").first()
        x.id = existing_user.id

        resualt = x.list_leader_project()
        self.assertEqual(resualt,[]) 
                      





if __name__ == "__main__":
    unittest.main()
