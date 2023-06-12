#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiClientConnectors:
    """
    A class for client connector related api calls.
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
            f"{self.org_id}/gateways"
        )

    def create(
        self, name, interface_name, dns_hosts=None, gateway_ips=None,
            group_ids=None, description="created by api user", tunnel=False
    ):
        """
        Used in the creation of client connectors.

        Args:
            - name (str): name of the client connector.
            - interface_name (str): interface to reach local lan.
            - dns_hosts (list(str)): not currently implemented.
            - gateway_ips (list(str)): not currently implemented.
            - group_ids (list(str)): not currently implemented.
            - description (str): meaningful description of the cc.
            - tunnel (boolean): not currently implemented.

        Returns:
            response (dict):
                - token (str): for installing the client connector.
                - user (dict): client connector object details.
        """

        dns_hosts = dns_hosts or []
        gateway_ips = gateway_ips or []
        group_ids = group_ids or []
        gateway_data = {
            "networkInterface": {
                "interfaceName": f"{interface_name}",
                "natDisabled": False
            },
            "name": f"{name}",
            "desc": f"{description}",
        }

        response = ApiHelper().http(
            "POST", self.session, self.url, payload=gateway_data
        )
        response = ApiHelper().parse(response["content"])
        return response

    def delete(self, name):
        """
        Used in the deletion of client connectors.

        Args:
            - name (str): name of the client connector.

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
        Shows configuration details for all client connectors.

        Returns:
            response (list(dict)): settings for all client connectors.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific client connector.

        Args:
            - name (str): name of the client connector.

        Returns:
            response (list(dict)): settings for a client connector.
        """

        for connector in self.get_all():
            if connector["name"] == name:
                user_id = connector["userId"]
                new_url = f"{self.url}/{user_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
