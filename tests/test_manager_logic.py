import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path
from logic.project_logic import project
from logic.task_logic import Tasks
from logic.user_logic import UserLogic, get_credentials_from_database_user_id
from logic.manager_logic import manager, check_is_user_active
from model.base_entity import UserEntity

u = UserLogic()
x = project(u)
dic = get_credentials_from_database_user_id()

m = manager()



class TestUserLogic(unittest.TestCase):
    # @patch("logic.user_logic.get_session")  # Adjust the import path as needed


    # def test_create_admin_admin_exist(self):

    #     result = m.create_admin('admin', '007')
    #     self.assertEqual(result, False)

    # def test_create_admin_correct(self):

    #     result = m.create_admin('new admin2', 'new password')
    #     self.assertEqual(result, True)
    
    def test_check_is_user_active_banned_user(self):
        result = check_is_user_active('b')
        self.assertEqual(result, False)
    
    def test_check_is_user_active_active_user(self):
        result = check_is_user_active('a')
        self.assertEqual(result, True)




        

if __name__ == "__main__":
    unittest.main()
