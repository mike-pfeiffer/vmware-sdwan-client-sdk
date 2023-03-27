#!/usr/bin/python3

from api_rules import ApiRules


class CliRules:
    """
    A class for rule api calls via the cli utility.
    """

    def create(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiRules().create(args.name)
        return output

    def delete(self, args):
        """
        Used to delete specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiRules().delete(args.name)
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
            output = ApiRules().get_all()
            return output

        elif args.name:
            output = ApiRules().get(args.name)
            return output
