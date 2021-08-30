from Database import DatabaseHandler

class LoginHandler:
    USERNAME = None
    def __init__(self, username=None):
        if username is not None:
            LoginHandler.USERNAME = username

    def log_user_in_handler(self, username, password): 
        """
        Method to log user in.
        
        Parameters:
            username (str) Username
            password (str) Password
        
        Returns:
            Username (str) or None if failed
        """
        return DatabaseHandler().log_user_in(username, password)


    def create_user_account_handler(self, username, password):
        """
        Method to create user account.
        
        Parameters:
            username (str) Username
            password (str) Password

        Returns:
            Last row index (int) or None if failed
        """  
        return DatabaseHandler().insert_user(username, password)
