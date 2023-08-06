from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import constants


# =========================================
# Custom help formatter for our argparser
# ==========================================
def cli_formatter():
    from argparse import HelpFormatter, _SubParsersAction

    class NoSubparsersMetavarFormatter(HelpFormatter):

        def _format_action(self, action):
            result = super(NoSubparsersMetavarFormatter,
                        self)._format_action(action)
            if isinstance(action, _SubParsersAction):
                return "%*s%s" % (self._current_indent, "", result.lstrip())
            return result

        def _format_action_invocation(self, action):
            if isinstance(action, _SubParsersAction):
                return ""
            return super(NoSubparsersMetavarFormatter,
                        self)._format_action_invocation(action)

        def _iter_indented_subactions(self, action):
            if isinstance(action, _SubParsersAction):
                try:
                    get_subactions = action._get_subactions
                except AttributeError:
                    pass
                else:
                    for subaction in get_subactions():
                        yield subaction
            else:
                for subaction in super(NoSubparsersMetavarFormatter,
                                    self)._iter_indented_subactions(action):
                    yield subaction
    
    return NoSubparsersMetavarFormatter



# ==================
# e2e Help messages
# ==================
def common_msg_part():
                    Py_version_manager.py_print()
                    Py_version_manager.py_print("E2E CLI")
                    Py_version_manager.py_print()
                    Py_version_manager.py_print("positional arguments:")
                    Py_version_manager.py_print("option       The option to be used or name of your access credentials")
                    Py_version_manager.py_print()
                    Py_version_manager.py_print("optional arguments:")
                    Py_version_manager.py_print( "-h, --help          To show this help message and exit")
                    Py_version_manager.py_print( "-v, --version       To see version info")
                    Py_version_manager.py_print( "--info              To show package info")
                    Py_version_manager.py_print()

def e2e_help():
                        Py_version_manager.py_print( "usage: e2e_cli {help/doc, alias, @<alias>}")
                        common_msg_part()
                        Py_version_manager.py_print( "Commands/Options:")
                        Py_version_manager.py_print( "    help/doc            To view detailed man doc")
                        Py_version_manager.py_print( "    alias               To add/delete api key and auth tokens")
                        Py_version_manager.py_print( "    @<alias>            To access services using CLI")
         
def e2e_alias_help():
                        Py_version_manager.py_print( "usage: e2e_cli alias {add, view, add_file, delete}")
                        common_msg_part()
                        Py_version_manager.py_print( "alias commands:")
                        Py_version_manager.py_print( "    add                 To add api key and auth token")
                        Py_version_manager.py_print( "    add_file            To add api key and auth token via file")
                        Py_version_manager.py_print( "    view                To view a list of tokens")
                        Py_version_manager.py_print( "    delete              To add delete api key and auth token")
        
def e2e_service_help():
                        Py_version_manager.py_print("usage: e2e_cli @<alias> [-h] {node,lb,bucket,dbaas,image,autoscaling,vpc,cdn,volumes} ...")
                        common_msg_part()
                        Py_version_manager.py_print( "Commands:")
                        Py_version_manager.py_print("node         To apply crud operations over Nodes")
                        Py_version_manager.py_print("lb           To apply operations over Load-Balancer")
                        Py_version_manager.py_print("bucket       To create/delete/list buckets of the user")
                        Py_version_manager.py_print("dbaas        To perform operations over DBaaS service provided")
                        Py_version_manager.py_print("image        To perform operations over Image service provided")
                        Py_version_manager.py_print("autoscaling  To create/delete/list autoscaling for the user")
                        Py_version_manager.py_print("vpc          To create/delete/list vpc for the user")
                        Py_version_manager.py_print("cdn          To create/delete/list cdn for the user")
                        Py_version_manager.py_print("volumes      To create/delete/list volume for the user")



# =========================
# e2e pkg/ver-info functions
# =========================
def e2e_version_info():
        Py_version_manager.py_print(constants.packagke_version)

def e2e_pakage_info():
        Py_version_manager.py_print(constants.packagke_info)
