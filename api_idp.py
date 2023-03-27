#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.2"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiIdp(object):
    """
    A class for user identity related api calls.
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
            f"{SDWC_BASE_URL}/register-accounts/{VERSION}/idps/api/"
            f"orgs/{self.org_id}/invs/roles"
        )

    def create(self, role_type, email, name):
        """
        Used in the creation of groups.

        Args:
            - role_type (str): assigned privileges.
            - email (str): user email address.
            - name (str): name of the user.

        Returns:
            response (str): http status code.
        """

        new_url = self.url + f"/{role_type}/emails/{email}"
        user_data = {
            "firstName": f"{name}"
        }

        response = ApiHelper().http(
            "POST", self.session, new_url, payload=user_data
        )

        response = ApiHelper().parse(response)
        response = response["status"]

        return response
