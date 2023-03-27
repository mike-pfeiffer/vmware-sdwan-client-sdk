#!/usr/bin/python3

import os
import requests
from api_helper import ApiHelper

VERSION = "v1.1"

try:
    SDWC_API_KEY = os.environ["SDWC_API_KEY"]
    SDWC_BASE_URL = os.environ["SDWC_BASE_URL"]
except KeyError:
    ApiHelper().print_env_error()


class ApiAuthenticate(object):
    """
    A class for authentication related api calls.
    """

    def __init__(self):
        """
        Initializes the authorization headers with the api key.

        Returns:
            None.
        """

        self.api_key = os.environ["SDWC_API_KEY"]
        self.headers = {
            "accept": "application/json;charset=UTF-8",
            "Authorization": f"{self.api_key}"
        }

    def login(self):
        """
        Executes login with provided api key. If successful, returns
        a session object with access token and provides org id number
        for subsequent api calls.

        Returns:
            dict:
                - session (obj): session header with access token.
                - org_id (str): the accounts org id number.
        """

        session = requests.Session()
        session.headers.update(self.headers)
        url = (
            f"{SDWC_BASE_URL}/login-accounts/{VERSION}/"
            "auths/apis/oauth/token"
        )
        auth = ApiHelper().http("POST", session, url)
        auth = ApiHelper().parse(auth["content"])
        token_type = auth["token_type"]
        access_token = auth["access_token"]
        org_id = auth["meta"]["orgId"]
        auth_header = {
            "authorization": f"{token_type} {access_token}"
        }
        session.headers.update(auth_header)
        return {"session": session, "org_id": org_id}
