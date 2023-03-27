#!/usr/bin/python3

import argparse
from cli_test import CliTest
from cli_users import CliUsers
from cli_rules import CliRules
from cli_helper import CliHelper
from cli_groups import CliGroups
from cli_servers import CliServers
from cli_contexts import CliContexts
from cli_networks import CliNetworks
from cli_client_connectors import CliClientConnectors

SHOW = "show"
CREATE = "create"
DELETE = "delete"

TEST = "test"
USERS = "users"
RULES = "rules"
GROUPS = "groups"
SERVERS = "servers"
NETWORKS = "networks"
CONTEXTS = "contexts"
CONNECTORS = "connectors"

ARG_ALL = "--all"
ARG_NAME = "--name"
ARG_DPORT = "--dport"
ARG_ROLE = "--role"
ARG_EMAIL = "--email"
ARG_TARGET = "--target"
ARG_SOURCE = "--source"
ARG_IFACE = "--interface"
ARG_PROTOCOL = "--protocol"
ARG_SUBDOMAIN = "--subdomain"


class Sdwc:
    """
    The main entry point for the sd-wan client cli utility for the sdk.
    This class provides interactive prompts by using argparse library.
    """

    def __init__(self):
        """
        Initializes the class with various parsers for the cli.

        Returns:
            None.
        """

        self.parser = argparse.ArgumentParser(
            description="SD-WAN Client API CLI"
        )

        self.subparsers = self.parser.add_subparsers(
            dest="command"
        )

        # BEGIN_SECTION: commands code block

        create_parser = self.subparsers.add_parser(
            f"{CREATE}",
            help="add an object"
        )

        create_subparsers = create_parser.add_subparsers(
            dest="object"
        )

        delete_parser = self.subparsers.add_parser(
            f"{DELETE}",
            help="remove an object"
        )

        delete_subparsers = delete_parser.add_subparsers(
            dest="object"
        )

        show_parser = self.subparsers.add_parser(
            f"{SHOW}",
            help="get object details"
        )

        show_subparsers = show_parser.add_subparsers(
            dest="object"
        )

        test_parser = self.subparsers.add_parser(
            f"{TEST}",
            help="validate configurations"
        )

        test_subparsers = test_parser.add_subparsers(
            dest="object"
        )

        # END_SECTION: commands code block

        # BEGIN_SECTION: test sub-commands

        test_network_parser = test_subparsers.add_parser(
            f"{NETWORKS}",
            help="test for network match"
        )

        test_network_parser.add_argument(
            f"{ARG_SOURCE}",
            required=True,
            help="the name of the traffic source"
        )

        test_network_parser.add_argument(
            f"{ARG_TARGET}",
            required=True,
            help="the destination IP, FQDN, domain, or node name"
        )

        test_network_parser.add_argument(
            f"{ARG_PROTOCOL}",
            required=True,
            help="icmp, tcp, udp or named service (e.g., rdp, dns, ftp)"
        )

        test_network_parser.add_argument(
            f"{ARG_DPORT}",
            required=False,
            help=(
                "destination port 0-65535, only needed if tcp or udp "
                "is specified"
            )
        )

        # END_SECTION: test sub-commands

        # BEGIN_SECTION: connector sub-commands

        create_connector_parser = create_subparsers.add_parser(
            f"{CONNECTORS}",
            help="create a new connector"
        )

        create_connector_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        create_connector_parser.add_argument(
            f"{ARG_IFACE}",
            required=True
        )

        delete_connector_parser = delete_subparsers.add_parser(
            f"{CONNECTORS}",
            help="delete existing connector"
        )

        delete_connector_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_connector_parser = show_subparsers.add_parser(
            f"{CONNECTORS}",
            help="retrieve connector details"
        )

        show_connector_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_connector_parser.add_argument(
            f"{ARG_NAME}",
            required=False,
            help="name of the connector"
        )

        # END_SECTION: connector sub-commands

        # BEGIN_SECTION: server sub-commands

        create_server_parser = create_subparsers.add_parser(
            f"{SERVERS}",
            help="create a new server"
        )

        create_server_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        create_server_parser.add_argument(
            f"{ARG_SUBDOMAIN}",
            required=True
        )

        delete_server_parser = delete_subparsers.add_parser(
            f"{SERVERS}",
            help="delete existing server"
        )

        delete_server_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_server_parser = show_subparsers.add_parser(
            f"{SERVERS}",
            help="retrieve server details"
        )

        show_server_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_server_parser.add_argument(
            f"{ARG_NAME}",
            required=False,
            help="name of the server"
        )

        # END_SECTION: server sub-commands

        # BEGIN_SECTION: user sub-commands

        create_user_parser = create_subparsers.add_parser(
            f"{USERS}",
            help="create a new user"
        )

        create_user_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        create_user_parser.add_argument(
            f"{ARG_ROLE}",
            required=True,
            help="standard, owner, admin"
        )

        create_user_parser.add_argument(
            f"{ARG_EMAIL}",
            required=True,
            help="email address"
        )

        delete_user_parser = delete_subparsers.add_parser(
            f"{USERS}",
            help="delete existing user"
        )

        delete_user_parser.add_argument(
            f"{ARG_NAME}",
            required=True,
            help="add \" around name if spaces present"
        )

        show_user_parser = show_subparsers.add_parser(
            f"{USERS}",
            help="retrieve user details"
        )

        show_user_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_user_parser.add_argument(
            f"{ARG_NAME}",
            required=False,
            help="add \" around name if spaces present"
        )

        # END_SECTION: user sub-commands

        # BEGIN_SECTION: rules sub-commands

        create_rule_parser = create_subparsers.add_parser(
            f"{RULES}",
            help="create a new rule"
        )

        create_rule_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        delete_rule_parser = delete_subparsers.add_parser(
            f"{RULES}",
            help="delete existing rule"
        )

        delete_rule_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_rule_parser = show_subparsers.add_parser(
            f"{RULES}",
            help="retrieve rules details"
        )

        show_rule_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_rule_parser.add_argument(
            f"{ARG_NAME}",
            required=False,
            help="add \" around name if spaces present"
        )

        # END_SECTION: user sub-commands

        # BEGIN_SECTION: context sub-commands

        create_context_parser = create_subparsers.add_parser(
            f"{CONTEXTS}",
            help="create a new context"
        )

        create_context_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        delete_context_parser = delete_subparsers.add_parser(
            f"{CONTEXTS}",
            help="delete existing connector"
        )

        delete_context_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_context_parser = show_subparsers.add_parser(
            f"{CONTEXTS}",
            help="retrieve context details"
        )

        show_context_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_context_parser.add_argument(
            f"{ARG_NAME}",
            required=False,
            help="add \" around name if spaces present"
        )

        # END_SECTION: user sub-commands

        # BEGIN_SECTION: group sub-commands

        create_group_parser = create_subparsers.add_parser(
            f"{GROUPS}",
            help="create a new group"
        )

        create_group_parser.add_argument(
            f"{ARG_NAME}", required=True
        )

        delete_group_parser = delete_subparsers.add_parser(
            f"{GROUPS}",
            help="delete existing group"
        )

        delete_group_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_group_parser = show_subparsers.add_parser(
            f"{GROUPS}",
            help="retrieve group details"
        )

        show_group_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_group_parser.add_argument(
            f"{ARG_NAME}", required=False,
            help="add \" around name if spaces present"
        )

        # END_SECTION: group sub-commands

        # BEGIN_SECTION: network sub-commands

        create_network_parser = create_subparsers.add_parser(
            f"{NETWORKS}", help="create a new network"
        )

        create_network_parser.add_argument(
            f"{ARG_NAME}", required=True
        )

        create_network_parser.add_argument(
            "--type",
            required=True,
            help="mesh or hub"
        )

        create_network_parser.add_argument(
            "--rule",
            required=True,
            help="name of rule"
        )

        create_network_parser.add_argument(
            "--context",
            required=True,
            help="name of context"
        )

        create_network_parser.add_argument(
            "--sources",
            required=True,
            help="list of nodes or groups in format \"a, b\""
        )

        create_network_parser.add_argument(
            "--destinations",
            required=False,
            help=(
                "(optional) only for hub and spoke network type, "
                "list of nodes or groups in format \"a, b\""
            )
        )

        create_network_parser.add_argument(
            "--keep-connected",
            required=False,
            help=(
                "(optional) defaults to false, can be set to "
                "\"true\" (not recommended)"
            )
        )

        delete_network_parser = delete_subparsers.add_parser(
            f"{NETWORKS}",
            help="delete existing network"
        )

        delete_network_parser.add_argument(
            f"{ARG_NAME}",
            required=True
        )

        show_network_parser = show_subparsers.add_parser(
            f"{NETWORKS}",
            help="retrieve network details"
        )

        show_network_parser.add_argument(
            f"{ARG_ALL}",
            required=False,
            action="store_true",
            help="hit enter after specifying this option"
        )

        show_network_parser.add_argument(
            f"{ARG_NAME}", required=False,
            help="add \" around name if spaces present"
        )

        # END_SECTION: network sub-commands

    def execute_command(self, args):
        """
        Provides command execution logic for the parsed input.

        Args:
            - args (object): parsed commands as argparse object.

        Returns:
            None.
        """

        if args.command == "create":

            if args.object == "connectors":
                result = CliClientConnectors().create(args)
                CliHelper().print_json(result)

            elif args.object == "servers":
                result = CliServers().create(args)
                CliHelper().print_json(result)

            elif args.object == "groups":
                result = CliGroups().create(args)
                CliHelper().print_json(result)

            elif args.object == "users":
                result = CliUsers().create(args)
                CliHelper().print_status(result)

            elif args.object == "networks":
                if args.type == "mesh":
                    result = CliNetworks().create_mesh(args)
                    CliHelper().print_json(result)
                elif args.type == "hub":
                    if args.destinations is None:
                        print("ERROR!")
                    result = CliNetworks().create_hub_spoke(args)
                    CliHelper().print_json(result)

            elif args.object == "contexts":
                result = CliContexts().create(args)
                CliHelper().print_json(result)

            elif args.object == "rules":
                result = CliRules().create(args)
                CliHelper().print_json(result)

        elif args.command == "delete":

            if args.object == "connectors":
                result = CliClientConnectors().delete(args)
                CliHelper().print_json(result)

            elif args.object == "servers":
                result = CliServers().delete(args)
                CliHelper().print_json(result)

            elif args.object == "users":
                result = CliUsers().delete(args)
                CliHelper().print_json(result)

            elif args.object == "groups":
                result = CliGroups().delete(args)
                CliHelper().print_json(result)

            elif args.object == "contexts":
                result = CliContexts().delete(args)
                CliHelper().print_json(result)

            elif args.object == "rules":
                result = CliRules().delete(args)
                CliHelper().print_json(result)

            elif args.object == "networks":
                result = CliNetworks().delete(args)
                CliHelper().print_json(result)

        elif args.command == "show":

            if args.object == "connectors":
                result = CliClientConnectors().show(args)
                CliHelper().print_json(result)

            elif args.object == "servers":
                result = CliServers().show(args)
                CliHelper().print_json(result)

            elif args.object == "users":
                result = CliUsers().show(args)
                CliHelper().print_json(result)

            elif args.object == "groups":
                result = CliGroups().show(args)
                CliHelper().print_json(result)

            elif args.object == "networks":
                result = CliNetworks().show(args)
                CliHelper().print_json(result)

            elif args.object == "rules":
                result = CliRules().show(args)
                CliHelper().print_json(result)

            elif args.object == "contexts":
                result = CliContexts().show(args)
                CliHelper().print_json(result)

        elif args.command == "test":

            if args.object == "networks":
                result = CliTest().find_network(args)
                CliHelper().print_json(result)


def main():
    """
    A driver for instantiating the sdwc object, retrieving input,
    and executing the commands.

    Returns:
        None.
    """
    sdwc = Sdwc()
    args = sdwc.parser.parse_args()
    sdwc.execute_command(args)


if __name__ == "__main__":
    main()
