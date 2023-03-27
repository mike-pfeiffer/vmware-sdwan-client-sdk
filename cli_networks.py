#!/usr/bin/python3

from api_rules import ApiRules
from api_users import ApiUsers
from api_groups import ApiGroups
from api_contexts import ApiContexts
from api_networks import ApiNetworks


class CliNetworks:
    """
    A class for network api calls via the cli utility.
    """

    def build_nodes_dict(self, nodes):
        """
        Used to convert nodes to their uuid and associate it
        with their specified node type.

        Args:
            - nodes (list): a list containing node names.

        Returns:
            nodes_dict (dict): a user/group dict with node ids.
        """

        user_list = []
        group_list = []

        for node in nodes:
            a_user = ApiUsers().get(node)
            a_group = ApiGroups().get(node)

            if a_user is not None:
                user_list.append(a_user["userId"])

            if a_group is not None:
                group_list.append(a_group["groupId"])

        nodes_dict = {
            "user": user_list,
            "group": group_list
        }

        return nodes_dict

    def create_hub_spoke(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        sources = args.sources
        sources = sources.split(",")
        sources = [elem.strip() for elem in sources]
        sources_dict = self.build_nodes_dict(sources)

        destinations = args.destinations
        destinations = destinations.split(",")
        destinations = [elem.strip() for elem in destinations]
        destinations_dict = self.build_nodes_dict(destinations)

        rule = ApiRules().get(args.rule)
        rule = rule["ruleId"]

        context = ApiContexts().get(args.context)
        context = context["contextId"]

        output = ApiNetworks().create_hub_spoke(
            args.name,
            sources_dict,
            destinations_dict,
            rule,
            context
        )

        return output

    def create_mesh(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        sources = args.sources
        sources = sources.split(",")
        sources = [elem.strip() for elem in sources]
        sources_dict = self.build_nodes_dict(sources)

        rule = ApiRules().get(args.rule)
        rule = rule["ruleId"]

        context = ApiContexts().get(args.context)
        context = context["contextId"]

        output = ApiNetworks().create_mesh(
            args.name,
            sources_dict,
            rule,
            context
        )

        return output

    def delete(self, args):
        """
        Used to delete specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiNetworks().delete(args.name)
        return output

    def show(self, args):
        """
        Used to show details about specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        if args.all:
            output = ApiNetworks().get_all()
            return output

        elif args.name:
            output = ApiNetworks().get(args.name)
            return output
