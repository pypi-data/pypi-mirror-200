import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.volumes.volumes_crud.volumes import volumes_Crud
from e2e_cli.volumes.volumes_actions.volumes_action import volumesActions

class volumes_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if (self.arguments.action is None) and (self.arguments.volumes_commands is None):
            subprocess.call(['e2e_cli', 'alias', 'volumes', '-h'])

        elif (self.arguments.volumes_commands is not None) and (self.arguments.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.volumes_commands == 'create':
            volumes_operations = volumes_Crud(alias=self.arguments.alias )
            if(volumes_operations.possible):
                        try:
                            volumes_operations.create_volumes()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.volumes_commands == 'delete':
            volumes_operations = volumes_Crud(alias=self.arguments.alias)
            if(volumes_operations.possible):
                        try:
                            volumes_operations.delete_volumes()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.volumes_commands == 'list':
            volumes_operations = volumes_Crud(alias=self.arguments.alias)
            if(volumes_operations.possible):
                        try:
                            volumes_operations.list_volumes()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        # elif self.arguments.action == "attach_volume":
        #     volumes_operations = volumesActions(alias=self.arguments.alias)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.attach_volume()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")

        # elif self.arguments.action == "desable_volumes":
        #     volumes_operations = volumesActions(alias=self.arguments.alias)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.disable_volumes()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")
        
        