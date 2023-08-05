import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.auto_scaling.auto_scaling import autoscaling_Crud

class autoscaling_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if (self.arguments.autoscaling_commands is None):
            subprocess.call(['e2e_cli', 'alias', 'autoscaling', '-h'])

        # elif (self.arguments.autoscaling_commands is not None) and (self.arguments.action is not None):
        #       Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.autoscaling_commands == 'create':
            auto_scaling_operations = autoscaling_Crud(alias=self.arguments.alias )
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.create_autoscaling()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.autoscaling_commands == 'delete':
            auto_scaling_operations = autoscaling_Crud(alias=self.arguments.alias)
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.delete_autoscaling()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.autoscaling_commands == 'list':
            auto_scaling_operations = autoscaling_Crud(alias=self.arguments.alias)
            if(auto_scaling_operations.possible):
                        try:
                            auto_scaling_operations.list_autoscaling()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")