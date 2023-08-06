"""This script handles the access token of the 42 API."""
import time
import requests

from . import config


class Api42Token:
    """A class for handling authentication tokens for the 42 API.

    Attributes:
        __token_url (str): The URL to request a new token from.
        __params (dict): The parameters to send in the token request.
        __token (dict): The current authentication token.
        __fetched_at (int): The timestamp when the current token was fetched.
    """

    def __init__(self) -> None:
        """Initializes a new Api42Token instance.

        Retrieves an initial authentication token and records the time it was
        fetched.
        """
        # Set up the URL and parameters for requesting a token.
        self.__token_url: str = config.token_url
        self.__params: dict = config.params
        # Fetch an initial token and record the time it was fetched.
        self.__token: dict = self.__get_token()
        self.__fetched_at = int(time.time())

    @property
    def token(self) -> dict:
        """Gets the current authentication token as a dictionary.

        Returns:
            dict: The current authentication token.
        """
        # Returns the current authentication token as a dictionary.
        return self.__token

    def __get_token(self) -> dict:
        """Sends a request to the token URL to retrieve a new authentication
        token.

        Raises:
            requests.exceptions.HTTPError: If the request to the token URL
            fails.

        Returns:
            dict: The new authentication token as a dictionary.
        """
        # Send a POST request to the token URL with the configured parameters.
        resp = requests.post(url=self.__token_url, params=self.__params, timeout=10)
        # Raise an exception if the request fails.
        resp.raise_for_status()
        # Return the JSON response as a dictionary.
        return resp.json()

    def needs_refresh(self) -> bool:
        """Returns True if Token needs to be refreshed.
        Returns:
            bool: True if Token needs to be refreshed, false otherwise.
        """
        return (self.token['expires_in'] - (int(time.time()) - self.__fetched_at)) <= 2

    def refresh(self) -> None:
        """Refreshes the current authentication token.

        If the current token has less than 2 seconds remaining before it
        expires, waits until it expires before refreshing the token.
        """
        # Calculate the time remaining until the token expires.
        time_left = self.__token['expires_in'] - \
            (time.time() - self.__fetched_at)
        # If the token has less than 2 seconds remaining, wait until it expires
        # before refreshing.
        if 0 < time_left <= 2:
            time.sleep(time_left)
        # Fetch a new token and record the time it was fetched.
        self.__token = self.__get_token()
        self.__fetched_at = int(time.time())

    def __str__(self) -> str:
        """Returns the access token as a string.

        Returns:
            str: The access token as a string.
        """
        # Return the access token as a string.
        return str(self.__token['access_token'])
