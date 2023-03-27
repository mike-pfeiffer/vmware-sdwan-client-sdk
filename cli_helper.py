#!/usr/bin/python3

import json


class CliHelper():
    """
    A class to assist with cli utility functionality.
    """

    def print_json(self, entry):
        """
        A simply printing function for sorting and indenting
        dictionary data.

        Args:
            - entry (dict): a dictionary to be printed.

        Returns:
            None
        """

        print(json.dumps(entry, sort_keys=True, indent=4))

    def print_status(self, entry):
        """
        A simply printing function for printing a status code.

        Args:
            - entry (dict): a dictionary to be printed.

        Returns:
            None
        """

        print(f"Status Code: {entry}")
