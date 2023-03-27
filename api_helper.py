#!/usr/bin/python3

import sys
import json
import requests


class ApiHelper():
    """
    A class for assisting other api libraries.
    """

    def __init__(self):
        """
        Initializes a dictionary for response data.

        Args:
            - http_resp_dict (dict): status, headers, content.

        Returns:
            None.
        """

        self.http_resp_dict = {
            "status": "",
            "headers": "",
            "content": ""
        }

    def http(self, method, session, url, payload=None):
        """
        Makes the http call to the api and parses the responses.

        Args:
            - method (str): http method such as GET or POST.
            - session (obj): requests library session object.
            - url (str): specified api endpoint.
            - payload (dict): configuration parameters.

        Returns:
            http_resp_dict (dict):
                - status (str): http status code for verification.
                - headers (dict): http response headers for troubleshooting.
                - content (dict): configuration details.

        Raises:
            - requests.exceptions.ConnectionError
            - requests.exceptions.HTTPError
            - requests.exceptions.URLRequired
            - requests.exceptions.TooManyRedirects
            - requests.exceptions.Timeout
            - requests.exceptions.RequestException
        """

        try:

            if method == "GET":
                response = session.get(url)
                self.http_resp_dict["status"] = response.status_code
                self.http_resp_dict["headers"] = response.headers
                self.http_resp_dict["content"] = response.content
                return self.http_resp_dict
            elif method == "POST":
                response = session.post(url, json=payload)
                self.http_resp_dict["status"] = response.status_code
                self.http_resp_dict["headers"] = response.headers
                self.http_resp_dict["content"] = response.content
                return self.http_resp_dict
        except requests.exceptions.ConnectionError as e:
            raise Exception(e)
        except requests.exceptions.HTTPError as e:
            raise Exception(e)
        except requests.exceptions.URLRequired as e:
            raise Exception(e)
        except requests.exceptions.TooManyRedirects as e:
            raise Exception(e)
        except requests.exceptions.Timeout as e:
            raise Exception(e)
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    def print_env_error(self):
        """
        A simple print message for issues related to not having the
        correct environment variables set. Will exit the program.

        Returns:
            None.
        """

        print(
            "Missing environment variable(s). Please run 'printenv' to"
            "\ndetermine which env var is missing. There should be values"
            "\nfor both SDWC_API_KEY and SDWC_BASE_URL. Consult the README"
            "\nif further assistance is needed."
        )
        sys.exit(1)

    def parse(self, data):
        """
        A simple parser for handling and structuring data.

        Returns:
            data(dict): structured data.

        Raises:
            - ValueError
            - json.decoder.JSONDecodeError
        """

        try:
            if isinstance(data, dict):
                return data
            else:
                data = json.loads(data)
                return data
        except ValueError as e:
            raise Exception(e)
        except json.decoder.JSONDecodeError as e:
            raise Exception(e)
