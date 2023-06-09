#!/usr/bin/python3

import os
from api_helper import ApiHelper
from api_authenticate import ApiAuthenticate

VERSION = "v1.1"

try:
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiContexts:
    """
    A class for context related api calls.
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
            f"{self.org_id}/contexts"
        )

    def create(
        self, name,
    ):
        """
        Used in the creation of contexts. Please note this function
        is under construction. At this time, the function can only
        create the context, but does not apply any desired settings.

        Args:
            - name (str): name of the context.

        Returns:
            response (list(dict)): settings for the context.
        """

        context_data = {
            "name": f"{name}",
            "description": "The description of my new context",
            "times": [{
                "start": {
                    "dateTime": None,
                    "tz": "America/Chicago",
                },
                "end": {
                    "dateTime": None,
                    "tz": "America/Chicago",
                },
                "recurrence": {
                    "cycle": {
                        "type": "WEEKDAYS",
                        "weekDays": [],
                        "period": 1,
                    },
                },
            },
            ],
            "status": "active",
            "allowType": "ALLOW",
            "new": True,
            "osTypes": [],
            "locations": [],
            "hasAntivirus": False,
            "hasScreenSaver": False,
        }

        response = ApiHelper().http(
            "POST", self.session, self.url, payload=context_data
        )
        response = ApiHelper().parse(response["content"])
        return response

    def delete(self, name):
        """
        Used in the deletion of contexts.

        Args:
            - name (str): name of the context.

        Returns:
            response (str): http status code.
        """

        del_headers = {
            "x-http-method-override": "DELETE"
        }
        self.session.headers.update(del_headers)
        context_id = self.get(name)["contextId"]
        new_url = self.url + f"/{context_id}"
        response = ApiHelper().http(
            "POST", self.session, new_url
        )
        response = response["status"]
        return response

    def get_all(self):
        """
        Shows configuration details for all contexts.r.

        Returns:
            response (list(dict)): settings for all contexts.
        """

        response = ApiHelper().http(
            "GET", self.session, self.url
        )
        response = ApiHelper().parse(response["content"])
        return response

    def get(self, name):
        """
        Shows configuration details for a specific context.

        Args:
            - name (str): name of the client connector.

        Returns:
            response (list(dict)): settings for a context.
        """

        for context in self.get_all():
            if context["name"] == name:
                context_id = context["contextId"]
                new_url = f"{self.url}/{context_id}"
                response = ApiHelper().http(
                    "GET", self.session, new_url
                )
                response = ApiHelper().parse(response["content"])
                return response
