import argparse
from functools import reduce

from e2e_cli.commands_routing import CommandsRouting
from e2e_cli.core.error_logs_service import ErrorLogs
from e2e_cli.core.py_manager import Py_version_manager, cli_formatter

class Main:
    def __init__(self):
        pass

    def FormatUsage(self, parser, action):
        format_string = "e2e_cli" + " alias"+ " " + action + " [-h]" + " {create,delete,list,edit/update} ... "
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " alias"+ " " + action + " [-h] " + command
        subparser_list = list(parser._subparsers._group_actions[0].choices.keys())
        subparser_string = "{ " + reduce(lambda a, b: a + ", " + b, subparser_list) + " }"
        format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h]" + " " + subparser_string
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h] " + command
        parser.usage = format_string

    def config(self, parser):
        config_sub_parser = parser.add_subparsers(title="Config Commands", dest="config_commands")
        config_add_sub_parser = config_sub_parser.add_parser("add", help="To add api key and auth token")
        config_delete_sub_parser = config_sub_parser.add_parser("delete", help="To delete api key and auth token")
        config_view_sub_parser = config_sub_parser.add_parser("view", help="To view all alias and credentials")
        self.FormatUsageCommand(config_add_sub_parser, "config", "add")
        self.FormatUsageCommand(config_delete_sub_parser, "config", "delete")
        self.FormatUsageCommand(config_view_sub_parser, "config", "view")

    def node(self, parser):
        node_sub_parser = parser.add_subparsers(title="node Commands", dest="node_commands")
        node_action=parser.add_argument('-action', '--action', help="Type of action to be performed your node")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=cli_formatter())
        node_get_sub_parser = node_sub_parser.add_parser("get", help="To get a list of all nodes", formatter_class=cli_formatter())
        self.FormatUsageCommand(node_action, "node", "actions")
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_get_sub_parser, "node", "get")

    def image(self, parser):
        image_sub_parser = parser.add_subparsers(title="image Commands", dest="image_commands")
        image_list=parser.add_argument('-list_by', '--list_by', help="attribute/property by which you want to list images")
        image_create_sub_parser = image_sub_parser.add_parser("create", help="To create a new image")
        image_delete_sub_parser = image_sub_parser.add_parser("delete", help="To delete a specific image")
        image_list_sub_parser = image_sub_parser.add_parser("list", help="To get a list of all image")
        image_get_sub_parser = image_sub_parser.add_parser("rename", help="To rename a specific image")
        self.FormatUsageCommand(image_list, "image", "list_by")
        self.FormatUsageCommand(image_create_sub_parser, "image", "create")
        self.FormatUsageCommand(image_delete_sub_parser, "image", "delete")
        self.FormatUsageCommand(image_list_sub_parser, "image", "list")
        self.FormatUsageCommand(image_get_sub_parser, "image", "rename")

    def lb(self, parser):
        node_sub_parser = parser.add_subparsers(title="LB Commands", dest="lb_commands")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=cli_formatter())
        node_edit_sub_parser = node_sub_parser.add_parser("edit", help="To get a list of all nodes", formatter_class=cli_formatter())
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_edit_sub_parser, "node", "edit")

    def bucket(self, parser):
        bucket_sub_parser = parser.add_subparsers(title="bucket Commands", dest="bucket_commands")
        bucket_action=parser.add_argument('-action', '--action', help="Type of action to be performed your bucket")
        bucket_create_sub_parser = bucket_sub_parser.add_parser("create", help="To create a new bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("delete", help="To delete a specific bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(bucket_action, "bucket", "actions")
        self.FormatUsageCommand(bucket_create_sub_parser, "bucket", "create")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "delete")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "list")    

    def autoscaling(self, parser):
        autoscaling_sub_parser = parser.add_subparsers(title="autoscaling Commands", dest="autoscaling_commands")
        autoscaling_create_sub_parser = autoscaling_sub_parser.add_parser("create", help="To create a new bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("delete", help="To delete a specific bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(autoscaling_create_sub_parser, "autoscaling", "create")
        self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "delete")
        self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "list")

    def vpc(self, parser):
        vpc_sub_parser = parser.add_subparsers(title="vpc Commands", dest="vpc_commands")
        vpc_create_sub_parser = vpc_sub_parser.add_parser("create", help="To create a new bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("delete", help="To delete a specific bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(vpc_create_sub_parser, "vpc", "create")
        self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "delete")
        self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "list")

    def cdn(self, parser):
        cdn_sub_parser = parser.add_subparsers(title="cdn Commands", dest="cdn_commands")
        cdn_action=parser.add_argument('-action', '--action', help="Type of action to be performed your cdn")
        cdn_create_sub_parser = cdn_sub_parser.add_parser("create", help="To create a new cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("delete", help="To delete a specific cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("list", help="To get a list of all cdn")
        self.FormatUsageCommand(cdn_action, "cdn", "actions")
        self.FormatUsageCommand(cdn_create_sub_parser, "cdn", "create")
        self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "delete")
        self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "list")

    def volumes(self, parser):
        volumes_sub_parser = parser.add_subparsers(title="volumes Commands", dest="volumes_commands")
        volumes_action=parser.add_argument('-action', '--action', help="Type of action to be performed your volumes")
        volumes_create_sub_parser = volumes_sub_parser.add_parser("create", help="To create a new volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("delete", help="To delete a specific volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("list", help="To get a list of all volumes")
        self.FormatUsageCommand(volumes_action, "volumes", "actions")
        self.FormatUsageCommand(volumes_create_sub_parser, "volumes", "create")
        self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "delete")
        self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "list")
           
    def dbaas(self, parser):
        dbaas_sub_parser = parser.add_subparsers(title="DBaaS Commands", dest="dbaas_commands")
        dbaas_action=parser.add_argument('-action', '--action', help="Type of action to be performed your dbaas")
        dbaas_create_sub_parser = dbaas_sub_parser.add_parser("create", help="To launch a new dbaas")
        dbaas_delete_sub_parser = dbaas_sub_parser.add_parser("delete", help="To delete a created dbaas")
        dbaas_list_sub_parser = dbaas_sub_parser.add_parser("list", help="To list all of your dbaas")
        self.FormatUsageCommand(dbaas_action, "dbaas", "actions")
        self.FormatUsageCommand(dbaas_create_sub_parser, "dbaas", "create")
        self.FormatUsageCommand(dbaas_list_sub_parser, "dbaas", "list")
        self.FormatUsageCommand(dbaas_delete_sub_parser, "dbaas", "delete")


class ArgPaser(argparse.ArgumentParser):
    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        print( args["message"])


def commanding(parser):
    sub_parsers = parser.add_subparsers(title="Commands", dest="command")
    alias_add_parser = sub_parsers.add_parser("add" )
    alias_add_parser = sub_parsers.add_parser("add_file" )
    alias_add_parser = sub_parsers.add_parser("view")
    alias_delete_parser= sub_parsers.add_parser("delete")
    node_parser = sub_parsers.add_parser("node", help="To apply crud operations over Nodes")
    lb_parser = sub_parsers.add_parser("lb", help="To apply operations over Load-Balancer")
    bucket_parser = sub_parsers.add_parser("bucket", help="To create/delete/list buckets of the user")
    dbaas_parser = sub_parsers.add_parser("dbaas", help="To perform operations over DBaaS service provided")
    image_parser = sub_parsers.add_parser("image", help="To perform operations over Image service provided")
    autoscaling_parser= sub_parsers.add_parser("autoscaling", help="To create/delete/list autoscaling for the user")
    vpc_parser= sub_parsers.add_parser("vpc", help="To create/delete/list vpc for the user")
    cdn_parser= sub_parsers.add_parser("cdn", help="To create/delete/list cdn for the user")
    volumes_parser= sub_parsers.add_parser("volumes", help="To create/delete/list volume for the user")
    m = Main()
    # m.config(config_parser)
    m.bucket(bucket_parser)
    m.node(node_parser)
    m.dbaas(dbaas_parser)
    m.lb(lb_parser)
    m.image(image_parser)
    m.autoscaling(autoscaling_parser)
    m.vpc(vpc_parser)
    m.cdn(cdn_parser)
    m.volumes(volumes_parser)

    # m.FormatUsage(config_parser, "config")
    m.FormatUsage(node_parser, "node")
    m.FormatUsage(lb_parser, "lb")
    m.FormatUsage(bucket_parser, "bucket")
    m.FormatUsage(dbaas_parser, "dbaas")
    m.FormatUsage(autoscaling_parser, "autoscaling")
    m.FormatUsage(vpc_parser, "vpc")
    m.FormatUsage(cdn_parser, "cdn")
    m.FormatUsage(volumes_parser, "volumes")


def run_main_class():
    parser = ArgPaser(description="E2E CLI", formatter_class=cli_formatter())
    parser.add_argument("alias", type=str, help="The name of your API access credentials")
    commanding(parser)

    args = parser.parse_args()
    commands_route = CommandsRouting(args)
    commands_route.route()
   
    

