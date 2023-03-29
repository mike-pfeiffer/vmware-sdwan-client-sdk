#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiUsers:
    """
    A class for user related api calls.
    """

    def __init__(self):
        """
        Initializes the class with the session and org_id provided
        by api_authenicate.py. Includes the url for all API calls
        relevant to functions in this class.

        Args:
            - auth (obj): auth object from api_authenticate.py.
            - session (obj): session header with access token.
            - org_id (str): the accounts org id number.
            - url (str): the url specific to this class's api endpoint.

        Returns:
            None.
        """

        self.auth = ApiAuthenticate().login()
        self.session = self.auth["session"]
        self.org_id = self.auth["org_id"]
        self.url = (
            f"{SDWC_BASE_URL}/manage-accounts/{VERSION}/api/orgs/"
            f"{self.org_id}/users"
        )

    def delete(self, name):
        """
        Used in the deletion of a user.

        Args:
            - name (str): name of the user.

        Returns:
            response (str): http status code.
        """

        del_headers = {
            "x-http-method-override": "DELETE"
        }
        self.session.headers.update(del_headers)
        user_id = self.get(name)["userId"]
        new_url = self.url + f"/{user_id}"
        response = ApiHelper().http(
            "POST", self.session, new_url
        )
        response = response["status"]
        return response

    def get_all(self):
        """
        Shows configuration details for all users.

        Returns:
            response (list(dict)): settings for all users.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific user.

        Args:
            - name (str): name of the user.

        Returns:
            response (list(dict)): settings for a user.
        """

        for user in self.get_all():
            if user["name"] == name:
                user_id = user["userId"]
                new_url = f"{self.url}/{user_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
