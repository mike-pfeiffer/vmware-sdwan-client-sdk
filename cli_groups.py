#!/usr/bin/python3

from api_groups import ApiGroups


class CliGroups:
    """
    A class for group api calls via the cli utility.
    """

    def create(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiGroups().create(args.name)
        return output

    def delete(self, args):
        """
        Used to delete specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiGroups().delete(args.name)
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
            output = ApiGroups().get_all()
            return output

        elif args.name:
            output = ApiGroups().get(args.name)
            return output
