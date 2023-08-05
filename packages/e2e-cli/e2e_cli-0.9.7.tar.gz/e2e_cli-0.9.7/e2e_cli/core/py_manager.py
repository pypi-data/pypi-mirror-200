from __future__ import print_function
import sys


# =========================================
# Print and Input manager for python 2 and 3
# ==========================================
class Py_version_manager:
    def __init__(self):
        pass

    @classmethod
    def py_input(self, msg):
        if(int(sys.version[0:1])<3):
                return raw_input(msg)
        else:
                return input(msg)
    
    @classmethod
    def py_print(self, *args):
        # if(int(sys.version[0:1])<3):
        #         print(*args, sep = " ")
        # else:
                print(*args, sep = " ")
                # return print(args)



# =========================================
# Customer help formatter for our argparser
# ==========================================

def py2_help_formatter():
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
       
       
def py3_help_formatter():
    from argparse import HelpFormatter, _SubParsersAction

    class NoSubparsersMetavarFormatter(HelpFormatter):

        def _format_action(self, action):
            result = super()._format_action(action)
            if isinstance(action, _SubParsersAction):
                # fix indentation on first line
                return "%*s%s" % (self._current_indent, "", result.lstrip())
            return result

        def _format_action_invocation(self, action):
            if isinstance(action, _SubParsersAction):
                # remove metavar and help line
                return ""
            return super()._format_action_invocation(action)

        def _iter_indented_subactions(self, action):
            if isinstance(action, _SubParsersAction):
                try:
                    get_subactions = action._get_subactions
                except AttributeError:
                    pass
                else:
                    # remove indentation
                    yield from get_subactions()
            else:
                yield from super()._iter_indented_subactions(action)
                
    return NoSubparsersMetavarFormatter


def cli_formatter():
    if(int(sys.version[0:1])<3):
            return  py2_help_formatter()
    else:
            return  py3_help_formatter()
        
