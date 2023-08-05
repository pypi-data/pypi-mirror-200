import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.vpc.vpc import vpc_Crud

class vpc_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if (self.arguments.vpc_commands is None):
            subprocess.call(['e2e_cli', 'alias', 'vpc', '-h'])

        # elif (self.arguments.vpc_commands is not None) and (self.arguments.action is not None):
        #       Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.vpc_commands == 'create':
            auto_scaling_operations = vpc_Crud(alias=self.arguments.alias )
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.create_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.vpc_commands == 'delete':
            auto_scaling_operations = vpc_Crud(alias=self.arguments.alias)
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.delete_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.vpc_commands == 'list':
            auto_scaling_operations = vpc_Crud(alias=self.arguments.alias)
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.list_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")