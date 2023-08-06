import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.node.node_crud.node import NodeCrud
from e2e_cli.node.node_actions.node_action import nodeActions

class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self):
        if (self.arguments.node_commands is None) and (self.arguments.action is None):
            subprocess.call(['e2e_cli', 'alias','node', '-h'])

        elif (self.arguments.node_commands is not None) and (self.arguments.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")
              
        if self.arguments.node_commands == 'create':
            Node_operations = NodeCrud(alias=self.arguments.alias )
            if(Node_operations.possible):
                        try:
                           Node_operations.create_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")  
                              

        elif self.arguments.node_commands == 'delete':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.delete_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        

        elif self.arguments.node_commands == 'get':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.get_node_by_id()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
                                    
        elif self.arguments.node_commands == 'list':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try: 
                           Node_operations.list_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        

        elif self.arguments.action == 'enable_recovery':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.enable_recovery()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'disable_recovery':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.disable_recovery()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'reinstall':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.reinstall()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'reboot':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.reboot()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'power_on':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.power_on()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'power_off':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.power_off()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'rename_node':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.rename_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'lock_vm':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.lock_vm()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'unlock_vm':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.unlock_vm()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action =='monitor':
            Node_operations=nodeActions(alias=self.arguments.alias)     
            if(Node_operations.possible):
                        try: 
                           Node_operations.node_monitoring()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        else:
            Py_version_manager.py_print("command not found")
