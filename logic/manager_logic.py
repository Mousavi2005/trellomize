import argparse

class manager(user):
    def __init__(self,password,user_name,gmail):
        super().__init__(password,user_name)
        self.gmail = gmail

    def display_info(self):
        print(f"user_name : {self.user_name}  passwprd : {self.password}  gmail : {self.gmail}")


parser = argparse.ArgumentParser()
parser.add_argument("create-admin")
parser.add_argument("--username-admin")
parser.add_argument("--password-admin")

args = parser.parse_args()



admin_name = args.username_admin
admin_pass = args.password_admin
# have to add these to database