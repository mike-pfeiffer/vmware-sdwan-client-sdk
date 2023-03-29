#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiNetworks:
    """
    A class for network related api calls.
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
            f"{self.org_id}/v2lans"
        )

    def create_hub_spoke(
        self, name, source_ids, destination_ids,
        rule_id, context_id, keep_connected="false"
    ):
        """
        Used to build a hub and spoke network.

        Args:
            - name (str): name of the network.
            - source_ids (dict): contains uuid and node type.
            - destination_ids (dict): contains uuid and node type.
            - rule_id (str): uuid of referenced rule.
            - context_id (str): uuid of referenced context.
            - keep_connected (bool): default false.

        Returns:
            response (list(dict)): node details.
        """

        source_nobs = []

        for key, value in source_ids.items():
            if key == "user":
                for user_id in value:
                    temp = {"id": user_id, "type": key}
                    source_nobs.append(temp)
            elif key == "group":
                for group_id in value:
                    temp = {"id": group_id, "type": key}
                    source_nobs.append(temp)

        target_nobs = []

        for key, value in destination_ids.items():
            if key == "user":
                for user_id in value:
                    temp = {"id": user_id, "type": key}
                    target_nobs.append(temp)
            elif key == "group":
                for group_id in value:
                    temp = {"id": group_id, "type": key}
                    target_nobs.append(temp)

        v2lan_data = {
            "isKeepConnected": f"{keep_connected}",
            "name": f"{name}",
            "policy": {
                "ruleIds": [f"{rule_id}"],
                "sourceContextId": f"{context_id}"
            },
            "topology": {
                "sourceNobs": source_nobs,
                "targetNobs": target_nobs,
                "type": "HUB"
            }
        }

        response = ApiHelper().http(
            "POST", self.session, self.url, payload=v2lan_data
        )
        response = ApiHelper().parse(response["content"])

        return response

    def create_mesh(
        self, name, source_ids, rule_id, context_id, keep_connected="false"
    ):
        """
        Used to build a full mesh network.

        Args:
            - name (str): name of the network.
            - source_ids (dict): contains uuid and node type.
            - rule_id (str): uuid of referenced rule.
            - context_id (str): uuid of referenced context.
            - keep_connected (bool): default false.

        Returns:
            response (list(dict)): node details.
        """

        source_nobs = []

        for key, value in source_ids.items():
            if key == "user":
                for user_id in value:
                    temp = {"id": user_id, "type": key}
                    source_nobs.append(temp)
            elif key == "group":
                for group_id in value:
                    temp = {"id": group_id, "type": key}
                    source_nobs.append(temp)

        v2lan_data = {
            "isKeepConnected": f"{keep_connected}",
            "name": f"{name}",
            "policy": {
                "ruleIds": [f"{rule_id}"],
                "sourceContextId": f"{context_id}"
            },
            "topology": {
                "sourceNobs": source_nobs,
                "type": "MESH"
            }
        }

        response = ApiHelper().http(
            "POST", self.session, self.url, payload=v2lan_data
        )
        response = ApiHelper().parse(response["content"])

        return response

    def delete(self, name):
        """
        Used in the deletion of a network.

        Args:
            - name (str): name of the networks.

        Returns:
            response (str): http status code.
        """

        del_headers = {
            "x-http-method-override": "DELETE"
        }
        self.session.headers.update(del_headers)
        v2lan_id = self.get(name)["v2lanId"]
        new_url = f"{self.url}/{v2lan_id}"
        response = ApiHelper().http(
            "POST", self.session, new_url
        )
        response = response["status"]
        return response

    def get_all(self):
        """
        Shows configuration details for all networks.

        Returns:
            response (list(dict)): settings for all networks.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific network.

        Args:
            - name (str): name of the network.

        Returns:
            response (list(dict)): settings for a network.
        """

        for v2lan in self.get_all():
            if v2lan["name"] == name:
                v2lan_id = v2lan["v2lanId"]
                new_url = f"{self.url}/{v2lan_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
