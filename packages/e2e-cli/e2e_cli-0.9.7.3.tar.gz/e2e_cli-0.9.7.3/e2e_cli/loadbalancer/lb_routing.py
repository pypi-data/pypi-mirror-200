import subprocess

from e2e_cli.core.py_manager import Py_version_manager 
from e2e_cli.loadbalancer.lb import LBClass


class LBRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.lb_commands is None:
            subprocess.call(['e2e_cli', "alias", 'lb', '-h'])

        elif self.arguments.lb_commands == 'create':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.create_lb()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.lb_commands == 'list' or self.arguments.lb_commands == 'ls':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.list_lb()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.lb_commands == 'delete':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.delete_lb()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.lb_commands == 'edit':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.edit_lb()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
