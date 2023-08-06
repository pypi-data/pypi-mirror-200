import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.cdn.cdn_crud.cdn import cdn_Crud
from e2e_cli.cdn.cdn_actions.cdn_action import cdnActions

class cdn_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if (self.arguments.action is None) and (self.arguments.cdn_commands is None):
            subprocess.call(['e2e_cli', 'alias', 'cdn', '-h'])

        elif (self.arguments.cdn_commands is not None) and (self.arguments.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.cdn_commands == 'create':
            cdn_operations = cdn_Crud(alias=self.arguments.alias )
            if(cdn_operations.possible):
                        try:
                            cdn_operations.create_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.cdn_commands == 'delete':
            cdn_operations = cdn_Crud(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.delete_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.cdn_commands == 'list':
            cdn_operations = cdn_Crud(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.list_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == "enable_cdn":
            cdn_operations = cdnActions(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.enable_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == "disable_cdn":
            cdn_operations = cdnActions(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.disable_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == "cdn_monitoring":
            cdn_operations = cdnActions(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.cdn_monitoring()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == "cdn_bandwidth_usage":
            cdn_operations = cdnActions(alias=self.arguments.alias)
            if(cdn_operations.possible):
                        try:
                            cdn_operations.cdn_bandwidth_usage()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")