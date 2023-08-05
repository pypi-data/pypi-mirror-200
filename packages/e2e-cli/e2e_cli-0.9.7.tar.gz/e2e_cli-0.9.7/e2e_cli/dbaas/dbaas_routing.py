import subprocess

from e2e_cli.dbaas.dbaas_crud.dbaas import DBaaSClass
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.dbaas.dbaas_actions.dbaas_action import DBaasAction



class DBaaSRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if (self.arguments.dbaas_commands is None) and (self.arguments.action is None):
            subprocess.call(['e2e_cli', "alias",'dbaas', '-h'])

        elif (self.arguments.dbaas_commands is not None) and (self.arguments.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.dbaas_commands == 'create':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
              dbaas_class_object.create_dbaas()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.dbaas_commands == 'list' or self.arguments.dbaas_commands == 'ls':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
                dbaas_class_object.list_dbaas()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.dbaas_commands == 'delete':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
                dbaas_class_object.delete_dbaas_by_name()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
        
        elif self.arguments.action == 'take_snapshot':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.take_snapshot()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'reset_password':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.reset_password()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'stop_db':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.stop_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'start_db':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.start_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'restart_db':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.restart_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'enable_backup':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.enable_backup()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'disable_backup':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.disable_backup()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'add_parameter_group':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.add_parameter_group()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'remove_parameter_group':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.remove_parameter_group()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'add_vpc':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.add_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
        elif self.arguments.action == 'remove_vpc':
            DBaas_operations=DBaasAction(alias=self.arguments.alias)     
            if(DBaas_operations.possible):
                        try: 
                           DBaas_operations.remove_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            