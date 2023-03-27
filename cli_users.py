#!/usr/bin/python3

from api_idp import ApiIdp
from api_users import ApiUsers


class CliUsers:
    """
    A class for user api calls via the cli utility.
    """

    def create(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiIdp().create(args.role, args.email, args.name)
        return output

    def delete(self, args):
        """
        Used to delete specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiUsers().delete(args.name)
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
            output = ApiUsers().get_all()
            return output

        elif args.name:
            output = ApiUsers().get(args.name)
            return output
