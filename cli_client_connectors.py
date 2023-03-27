#!/usr/bin/python3

from api_client_connectors import ApiClientConnectors


class CliClientConnectors:
    """
    A class for client connector api calls via the cli utility.
    """

    def create(self, args):
        """
        Used to build specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiClientConnectors().create(args.name, args.interface)
        return output

    def delete(self, args):
        """
        Used to delete specified object type.

        Args:
            - args (obj): argparse object containing config details.

        Returns:
            output: response details from action.
        """

        output = ApiClientConnectors().delete(args.name)
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
            output = ApiClientConnectors().get_all()
            return output

        elif args.name:
            output = ApiClientConnectors().get(args.name)
            return output
