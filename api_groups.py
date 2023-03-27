#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiGroups(object):
    """
    A class for group related api calls.
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
            f"{self.org_id}/groups"
        )

    def create(self, name, description="created by api user"):
        """
        Used in the creation of groups.

        Args:
            - name (str): name of the group.
            - description (str): meaningful description of the group.

        Returns:
            response (list(dict)): settings for the context.
        """

        group_data = {
            "desc": f"{description}",
            "name": f"{name}",
        }

        group = ApiHelper().http(
            "POST", self.session, self.url, payload=group_data
        )
        group = ApiHelper().parse(group["content"])
        return group

    def delete(self, name):
        """
        Used in the deletion of groups.

        Args:
            - name (str): name of the groups.

        Returns:
            response (str): http status code.
        """

        del_headers = {
            "x-http-method-override": "DELETE"
        }
        self.session.headers.update(del_headers)
        group_id = self.get(name)["groupId"]
        delete_url = self.url + f"/{group_id}"
        request = self.session.post(delete_url, headers=del_headers)
        return request.status_code

    def get_members(self, name):
        """
        Finds nodes assigned to a specific group.

        Args:
            - name (str): name of the context.

        Returns:
            response (list(dict)): node details.
        """

        group_id = self.get(name)["groupId"]
        new_url = f"{self.url}/{group_id}/users"
        response = ApiHelper().http(
            "GET", self.session, new_url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get_all(self):
        """
        Shows configuration details for all groups.

        Returns:
            response (list(dict)): settings for all groups.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific group.

        Args:
            - name (str): name of the group.

        Returns:
            response (list(dict)): settings for a group.
        """

        for group in self.get_all():
            if group["name"] == name:
                group_id = group["groupId"]
                new_url = f"{self.url}/{group_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
