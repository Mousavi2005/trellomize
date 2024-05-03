class user:
    def __init__(self,password,user_name):
        self.password = password
        self.user_name = user_name

    def display_info(self):
        print(f"user_name : {self.user_name}  passwprd : {self.password}")

    def get_password_for_new_account(self):
        password = input("Enter password: ")
        if len(password) < 8 :
            print("Your password must have at least 8 characters")
        # here we have to check if password is reapeted
        # if not add it to database

    def check_login_password(password):
        pass
        # here we have to check if password is in database
    
    def get_username_for_new_account():
        username = input("User name : ")
        if len(username) <=3 :
            print("Your user name must have atleat 4 charachters")
        # here we have to check if username is in database
        # if not add it to database
    
temp = user(44,"Amin")
print(temp.display_info())