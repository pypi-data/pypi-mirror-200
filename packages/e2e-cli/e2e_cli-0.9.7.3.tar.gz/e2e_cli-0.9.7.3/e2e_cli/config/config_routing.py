import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.config.config import AuthConfig
from e2e_cli.core.alias_service import get_user_cred

class ConfigRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.command == 'add':
            try:
                api_key = Py_version_manager.py_input("Enter your api key: ")
                auth_token = Py_version_manager.py_input("Enter your auth token: ")
                auth_config_object = AuthConfig(alias=Py_version_manager.py_input("Input name of alias you want to add : "),
                                                    api_key=api_key,
                                                    api_auth_token=auth_token)
                auth_config_object.add_to_config()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
                pass


        elif self.arguments.command == 'add_file':
                path=Py_version_manager.py_input("input the file path : ")
                auth_config_object = AuthConfig()
                auth_config_object.adding_config_file(path)
                return
            

        elif self.arguments.command == 'delete':            
            confirmation =Py_version_manager.py_input("are you sure you want to delete press y for yes, else any other key : ")
            if(confirmation.lower()=='y'):
                auth_config_object = AuthConfig(alias=Py_version_manager.py_input("Input name of alias you want to add : "))
                try:
                    auth_config_object.delete_from_config()
                except:
                    pass  


        elif self.arguments.command == 'view':
                
                for item in list(get_user_cred("all", 1)):
                    Py_version_manager.py_print(item)
            

