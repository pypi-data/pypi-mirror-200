

from e2e_cli.core.error_logs_service import action_on_exception
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import help_messages

from e2e_cli.config.config_routing import ConfigRouting
from e2e_cli.loadbalancer.lb_routing import LBRouting
from e2e_cli.node.node_routing import NodeRouting
from e2e_cli.bucket_store.bucket_routing import BucketRouting
from e2e_cli.dbaas.dbaas_routing import DBaaSRouting
from e2e_cli.image.image_routing import ImageRouting
from e2e_cli.auto_scaling.autoscaling_routing import autoscaling_Routing
from e2e_cli.cdn.cdn_routing import cdn_Routing
from e2e_cli.vpc.vpc_routing import vpc_Routing
from e2e_cli.volumes.volumes_routing import volumes_Routing
from e2e_cli.man_display import man_page

class CommandsRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.alias is None:
                help_messages.e2e_help()


        elif self.arguments.alias == "help" or self.arguments.alias == "doc":
                man_page()


        elif (self.arguments.alias == "alias") :

            if(self.arguments.command not in ["add", "view","add_file","delete"]):
                help_messages.e2e_alias_help()  

            elif self.arguments.command in ["add", "view", "add_file", "delete"]:
                try:
                    ConfigRouting(self.arguments).route()
                except Exception as e:
                        Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.alias, traceback.print_exc())

    
        elif (self.arguments.alias[0]=="@"):

            if (self.arguments.command is None):
                Py_version_manager.py_print("issue in command/Wrong command given!!")
                help_messages.e2e_service_help()
                # subprocess.call(['e2e_cli', 'alias','-h'])

            elif self.arguments.command == "node":
                try:
                    NodeRouting(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)

            elif self.arguments.command == "lb":
                try: 
                    LBRouting(self.arguments).route()
                except Exception as e:
                        Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.alias, traceback.print_exc()) 
    
            elif self.arguments.command == "bucket":
                try:
                    BucketRouting(self.arguments).route()
                except Exception as e:
                        Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.alias, traceback.print_exc())
            
            elif self.arguments.command == "dbaas":
                try:
                    DBaaSRouting(self.arguments).route()
                except Exception as e:
                        Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.alias, traceback.print_exc())

            elif self.arguments.command == "image":
                try:
                    ImageRouting(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())   

            elif self.arguments.command == "autoscaling":
                try:
                    autoscaling_Routing(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())   
        
            elif self.arguments.command == "cdn":
                try:
                    cdn_Routing(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc()) 

            elif self.arguments.command == "vpc":
                try:
                    vpc_Routing(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())  

            elif self.arguments.command == "volumes":
                try:
                    volumes_Routing(self.arguments).route()
                except Exception as e:
                            Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())  
    
                            
        else :
              Py_version_manager.py_print("Command not found")
              Py_version_manager.py_print("Did you mean, e2e_cli help/doc --> for viewing man doc ??")
              Py_version_manager.py_print("Did you mean, e2e_cli alias [command] --> for adding alias ??")
              Py_version_manager.py_print("Did you mean, e2e_cli @<alias> [command] [sub-command] --> for accessing services ??")