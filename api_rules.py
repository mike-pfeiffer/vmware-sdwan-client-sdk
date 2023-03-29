#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiRules:
    """
    A class for rule related api calls.
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
            f"{self.org_id}/rules"
        )

    def create(
        self, name,
    ):
        """
        Used to build a rule. This function is not fully implemented
        so you are only able to create a named rule with no details.

        Args:
            - name (str): name of the rule.

        Returns:
            response (list(dict)): node details.
        """

        rule_data = {
            "name": f"{name}",
            "status": "active",
            "allowType": "ALLOW",
            "new": True,
            "predefinedNetworkServices": [],
        }

        response = ApiHelper().http(
            "POST", self.session, self.url, payload=rule_data
        )
        response = ApiHelper().parse(response["content"])
        return response

    def delete(self, name):
        """
        Used in the deletion of a rule.

        Args:
            - name (str): name of the rule.

        Returns:
            response (str): http status code.
        """

        del_headers = {
            "x-http-method-override": "DELETE"
        }
        self.session.headers.update(del_headers)
        rule_id = self.get(name)["ruleId"]
        new_url = self.url + f"/{rule_id}"
        response = ApiHelper().http(
            "POST", self.session, new_url
        )
        response = response["status"]
        return response

    def get_all(self):
        """
        Shows configuration details for all rules.

        Returns:
            response (list(dict)): settings for all rules.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific rule.

        Args:
            - name (str): name of the rule.

        Returns:
            response (list(dict)): settings for a rule.
        """

        for rule in self.get_all():
            if rule["name"] == name:
                rule_id = rule["ruleId"]
                new_url = f"{self.url}/{rule_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
