"""This script handles the requests made for the 42 API."""
from typing import Dict
from math import ceil
from multiprocessing.pool import ThreadPool
import time
import logging
import requests

from . import config
from .api42_token import Api42Token


class Api42RequestError(Exception):
    """Exception for requests errors raised in Api42."""


class Api42Request:
    """A class representing a request to the api."""

    def __init__(self, url: str, data: Dict = None, params: Dict = None):
        """
        Initializes an instance of Api42Request.

        Args:
            url (str): The URL of the request.
            data (Dict, optional): The body of the request. Defaults to None.
            params (Dict, optional): The parameters of the request. Defaults to
            None.
        """
        # Set the url attribute of the instance to the value of the url
        # parameter.
        self.url = url
        # Set the data attribute of the instance to the value of the data
        # parameter, or an empty dictionary if data is None.
        self.data = data if data is not None else {}
        # Set the params attribute of the instance to the value of the params
        # parameter, or an empty dictionary if params is None.
        self.params = params if params is not None else {}


class Api42:
    """
    A class that handles the requests made to the 42 API.

    Methods:
        __init__(self, requests_per_second: int = 4, log_lvl: str = 'WARNING',
                 raises: bool = False) -> None:
            Initializes an instance of the Api42 class with the given parameters.
            
        raises(self) -> bool:
            Returns the value of the raises attribute.

        raises(self, raises: bool) -> None:
            Sets the value of the raises attribute.

        log_lvl(self) -> str:
            Gets the log level.

        log_lvl(self, lvl: str) -> None:
            Sets the log level.

        requests_per_second(self) -> int:
            Gets the maximum number of requests per second.

        requests_per_second(self, rps: int) -> None:
            Sets the maximum number of requests per second.

        get(self, url: str, params: dict = {}, handle_pagination: bool = True,
            threaded: bool = True) -> list:
            Returns the result of a GET request.

        post(self, url: str, data: dict = {}):
            Returns the result of a POST request.

        patch(self, url: str, data: dict = {}):
            Returns the result of a PATCH request.

        put(self, url: str, data: dict = {}):
            Returns the result of a PUT request.

        delete(self, url: str, data: dict = {}):
            Returns the result of a DELETE request.
    """

    def __init__(self, requests_per_second: int = 4, log_lvl: str = 'WARNING',
                 raises: bool = False) -> None:
        """Constructs an instance of the Api42 class with the given parameters.

        Args:
            requests_per_second (int, optional): The maximum number of requests
                per second to make to the 42 API. Defaults to 4.
            log_lvl (str, optional): The log level. Defaults to 'WARNING'.
            raises (bool, optional): Whether exceptions should be raised or
                not. Defaults to False.
        """
        # Set log level based on given input. If input is not in
        # config.log_lvls, default to logging.WARNING.
        # Get logger and set log level.
        self.__log_lvl: int = config.log_lvls.get(log_lvl)
        if not self.__log_lvl:
            self.__log_lvl = logging.WARNING
            self.__log: logging.Logger = self.__get_logger()
            self.__log.warning(
                f'log: failed to recognize {log_lvl}, defaulting to WARNING')
        else:
            self.__log: logging.Logger = self.__get_logger()
        # Set base URL, API token, and headers.
        self.__base_url: str = config.api_url
        self.__token: Api42Token = Api42Token()
        self.__headers: dict = {'Authorization': f'Bearer {self.__token}'}
        # Set whether exceptions should be raised or not.
        self.__raises: bool = raises
        # Set maximum number of requests per second to make to 42 API
        if requests_per_second < 1:
            raise ValueError(f'{rps}: invalid value for requests_per_second')
        self.__requests_per_second: int = requests_per_second
        # logging Token
        self.__log.debug(f'{self.__headers}')

    def __get_logger(self) -> logging.Logger:
        """Creates a logger object and sets the log level, formatter, and
        handler for it.

        Returns:
            logging.Logger: The logger object.
        """
        # Create logger object and set name.
        logger: logging.Logger = logging.getLogger('Api42')
        # Create stream handler for logger.
        handler = logging.StreamHandler()
        # Create formatter for logger.
        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            datefmt='%d-%m-%y %H:%M:%S')
        # Set formatter for handler.
        handler.setFormatter(formatter)
        # Clear any existing handlers and add new handler.
        logger.handlers = []
        logger.addHandler(handler)
        # Set logger level.
        logger.setLevel(self.__log_lvl)
        return logger

    @property
    def raises(self) -> bool:
        """Gets the value of the raises attribute.

        Returns:
            bool: The value of the raises attribute.
        """
        return self.__raises

    @raises.setter
    def raises(self, raises: bool) -> None:
        """Sets the value of the raises attribute.

        Args:
            raises (bool): The value to set the raises attribute to.
        """
        self.__raises = raises

    @property
    def log_lvl(self) -> str:
        """Gets the log level.

        Returns:
            str: The log level.
        """
        return {v: k for k, v in config.log_lvls.items()}[self.__log_lvl]

    @log_lvl.setter
    def log_lvl(self, lvl: str) -> None:
        """Set the log level.

        Args:
            lvl (str): The new log level to set.

        Raises:
            ValueError: If the given log level is not valid.
        """
        # If given log level is not in config.log_lvls an Exception is raised
        if lvl not in set(config.log_lvls.keys()):
            raise ValueError(f'{lvl}: invalid value for log_lvl')
        # Set self.__log_lvl to value associated with given log level.
        self.__log_lvl = config.log_lvls[lvl]
        self.__log.setLevel(self.__log_lvl)

    @property
    def requests_per_second(self) -> int:
        """Sets the requests_per_second

        Returns:
            int: the number of requests the api is able to do per second.
        """
        # Getter for self.__requests_per_second
        return self.__requests_per_second

    @requests_per_second.setter
    def requests_per_second(self, rps: int) -> None:
        """Set the maximum number of requests per second to make to the 42API.

        Args:
            rps (int): The new maximum number of requests per second.

        Raises:
            ValueError: If rps is less than 1 and self.__raises is True.
        """
        # If given requests per second is less than 1, an exception is raised
        if rps < 1:
            raise ValueError(f'{rps}: invalid value for requests_per_second')
        self.__requests_per_second = rps

    def __refresh_token(self) -> None:
        """Refreshes the API token if needed."""
        # refreshing token if needed
        if self.__token.needs_refresh():
            self.__token.refresh()

    def get_token_info(self) -> dict:
        """Returns information about the current access token.
    
        The method first refreshes the access token if it has expired. It then
        sends a GET request to the token information endpoint and returns the 
        response body as a dictionary.
        
        Returns:
            A dictionary containing information about the current access token.
        
        Raises:
            Api42RequestError: If the request fails and `self.__raises` is
                True.
        """
        # Refresh the access token if needed
        self.__refresh_token()

        # Making the request
        url: str = f'{config.token_url}/info'
        resp = requests.get(url=url, headers=self.__headers)

        # Check if the response is successful
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Log an error message and raise an exception if the request fails
            self.__log.error(f'GET {resp.url} {resp.status_code}')
            if self.__raises:
                raise Api42RequestError(f'Failed: {e}') from e
            return {}

        # Return the response body as a dictionary
        return resp.json()

    def req_handler(func):
        def __req_handle(self, url: str, data: dict = {}):
            """This is a decorator method that adds an error-handling wrapper
            to the HTTP request methods. 
            
            It refreshes the access token if it has expired. It then calls the
            decorated method, and handles errors raised by the request.
            
            Args:
                url (str): The URL to send the HTTP request to.
                data (dict, optional): A dictionary of request data to include
                    in the HTTP request.
                    
            Returns:
                The response body of the HTTP request. If an error occurs while
                getting the response, an empty dictionary is returned.
            """
            # Refresh the access token if needed
            self.__refresh_token()

            # calling method function
            resp = func(self, url, data)

            # creating request string for logger
            request: str = f'{resp.request.method} {resp.url}'

            # Check for errors in the response
            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Log the error and optionally raise an exception
                self.__log.error(
                    f'{request} {resp.status_code}: {resp.reason}'
                    f'\n\tHeaders: {resp.headers}'
                    f'\n\tContent: {resp.content or {}}'
                )
                if self.__raises:
                    raise Api42RequestError(
                        f'{request}: {e}'
                    ) from e

            # Log the successful request
            self.__log.debug(f'{request} {resp.status_code}: {resp.reason}')

            # return the request in json format if possible else return content
            try:
                return resp.json()
            except requests.exceptions.JSONDecodeError:
                return resp.content or {}

        return __req_handle

    def get(self, url: str, params: dict = {}, handle_pagination: bool = True,
            threaded: bool = True) -> list:
        """Makes a GET request to the given URL and returns the response as a
        list.

        Refreshes the access token if it has expired.

        Args:
            url (str): The URL to send the GET request to.
            params (dict, optional): dictionary of query string parameters to
                include in the request.
            handle_pagination (bool, optional): If True, pagination information
                in the response headers will be used to retrieve additional
                pages of results.
            threaded (bool, optional): If True, additional pages of results
                will be requested in parallel.

        Returns:
            A list containing the response content. If an error occurs while
            getting the content, an empty list is returned.
        """
        # Refresh the access token if needed
        self.__refresh_token()

        # Set a default page size and number if none is given in the parameters
        if 'page' not in params:
            params['page'] = {'size': 100, 'number': 1}

        # Making the request
        endpoint: str = f'{self.__base_url}{url}'
        resp = requests.get(url=endpoint, json=params, headers=self.__headers)

        try:
            # Check for errors in the response
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Log the error and optionally raise an exception
            self.__log.error(
                f'GET {resp.url} {resp.status_code}: {resp.reason}'
                f'\n\tHeaders: {resp.headers}'
                f'\n\tContent: {resp.content or {}}'
            )
            if self.__raises:
                raise Api42RequestError(f'Failed: {e}') from e
            return []

        # Log the successful request
        self.__log.debug(f'GET {resp.url} {resp.status_code}: {resp.reason}')

        # Extract the response content as JSON
        results: list = resp.json()

        # Handle pagination if requested and if the response contains
        # pagination information
        if handle_pagination and ('X-Total' and 'X-Per-Page') in resp.headers:
            # Calculate the number of pages required to get all the results
            total = int(resp.headers['X-Total'])
            per_page = int(resp.headers['X-Per-Page'])
            npage = ceil(total / per_page)

            # Prepare a list of additional requests to get the remaining
            # pages of results
            reqs: list = []
            for i in range(2, npage + 1):
                pparams: dict = {}
                pparams.update(params)
                pparams['page'] = {'number': i, 'size': 100}
                reqs.append(Api42Request(url=url, params=pparams))

            # Use the mass_request method to send all the additional
            # requests in parallel (if requested)
            content = self.mass_request('GET', reqs, threaded=threaded)
            results.extend(content)

        # Return the list of results
        return results

    @ req_handler
    def post(self, url: str, data: dict = {}):
        """Sends a POST request to the given URL.

        If the access token has expired, it is refreshed before making the
        request.

        Args:
            url (str): The URL to send the POST request to.
            data (dict, optional): A dictionary of the body of the request to
                include in the request. Defaults to None.

        Returns:
            The response from the server.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        endpoint: str = f'{self.__base_url}{url}'
        resp = requests.post(url=endpoint, json=data, headers=self.__headers)
        # Return the result
        return resp

    @ req_handler
    def patch(self, url: str, data: dict = {}):
        """Makes a PATCH request to the given URL and returns the response.

        Refreshes the access token if it has expired.

        Args:
            url (str): The URL to send the PATCH request to.
            data (dict, optional): dictionary of the body of the request to
                include in the request.

        Returns:
            The response content. If an error occurs while getting the content,
            an empty list is returned.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        endpoint: str = f'{self.__base_url}{url}'
        resp = requests.patch(url=endpoint, json=data, headers=self.__headers)
        # Return the result
        return resp

    @ req_handler
    def put(self, url: str, data: dict = {}):
        """Makes a PUT request to the given URL and returns the response.

        Refreshes the access token if it has expired.

        Args:
            url (str): The URL to send the PUT request to.
            data (dict, optional): dictionary of the body of the request to
                include in the request.

        Returns:
            requests.Response: The response from the API endpoint.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        endpoint: str = f'{self.__base_url}{url}'
        resp = requests.put(url=endpoint, json=data, headers=self.__headers)
        # Return the result
        return resp

    @ req_handler
    def delete(self, url: str, data: dict = {}):
        """Send a DELETE request to the given URL and return the response.

        Refreshes the access token if it has expired.

        Args:
            url (str): The URL to send the DELETE request to.
            data (dict, optional): dictionary of the body of the request to
                include in the request.

        Returns:
            The response content. If an error occurs while getting the content,
            an empty list is returned.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        endpoint: str = f'{self.__base_url}{url}'
        resp = requests.delete(url=endpoint, json=data, headers=self.__headers)
        # Return the result
        return resp

    def mass_request(self, method: str, requests: list,
                     threaded: bool = True) -> list:
        """Performs multiple HTTP requests using the specified HTTP method and
       a list of requests.

        Args:
            method (str): The HTTP method to use. Must be one of: 'GET',
                'POST', 'PUT', 'PATCH', 'DELETE'.
            requests (list): A list of request objects to be sent. Each request
                should be a dictionary with the necessary parameters for the
                specified HTTP method.
            threaded (bool, optional): Whether to send the requests in parallel
                using multiple threads. Defaults to True.

        Returns:
            A list of responses from the API.

        Raises:
            ValueError: If the specified HTTP method is not recognized.
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Added sleep as a precaution for 2 mass_request calls
        time.sleep(1)
        # Getting correct method function
        func = {
            'GET': self.__get,
            'POST': self.__post,
            'PUT': self.__put,
            'PATCH': self.__patch,
            'DELETE': self.__delete
        }.get(method)
        # Log error and raise exception if get(method) fails
        if not func:
            self.__log.error(f'Method unrecognized: {method}')
            raise ValueError(f'Method unrecognized: {method}')

        results: list = []
        if threaded:
            def chunks(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            pools = chunks(requests, self.__requests_per_second)

            delta_time: float = 0
            start_time: float = 0

            for p in pools:

                if start_time > 0:
                    delta_time = 1.3 - (time.time() - start_time)
                if delta_time > 0:
                    time.sleep(delta_time)
                start_time = time.time()

                thpool = ThreadPool(processes=len(p))
                reqs = []
                for req in p:
                    reqs.append(
                        thpool.apply_async(
                            func,
                            (req,))
                    )

                resp_dicts = [r.get() for r in reqs]
                pres = []
                thpool.close()
                for i in range(len(resp_dicts)):
                    if isinstance(resp_dicts[i], list):
                        pres.extend(resp_dicts[i])
                    else:
                        pres.append(resp_dicts[i])

                results.extend(pres)

        else:
            for req in requests:
                resp = func(req)
                results.extend(resp.json())

        return results

    def handler(func):
        """Decorator that handles a request.

        Args:
            func (callable): The decorated function.

        Returns:
            callable: The decorated function.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        def __handle(self, request: Api42Request):
            """Handles the API request and logs the response.

            Args:
                request (Api42Request): The request object.

            Returns:
                dict or list: The response content in JSON format, or an empty
                dictionary or list if there is no content.

            Raises:
                Api42RequestError: If an error occurs while making the request
                    and `self.__raises` is set to True.
            """
            # Refresh the access token if needed
            self.__refresh_token()

            resp = func(self, request)

            # creating request string for logger
            req: str = f'{resp.request.method} {resp.url}'

            # Check for errors in the response
            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Log the error and optionally raise an exception
                self.__log.error(
                    f'{req} {resp.status_code}: {resp.reason}'
                    f'\n\tHeaders: {resp.headers}'
                    f'\n\tContent: {resp.content or {}}'
                )
                if self.__raises:
                    raise Api42RequestError(f'{req}: {e}') from e
            # Log the successful request
            self.__log.debug(f'{req} {resp.status_code}: {resp.reason}')

            # return the request in json format if possible else return content
            try:
                return resp.json()
            except requests.exceptions.JSONDecodeError:
                return resp.content or {}

        return __handle

    @handler
    def __get(self, req: Api42Request) -> requests.Response:
        """Sends a GET request and handles the response.

        Args:
            req (Api42Request): The request object.

        Returns:
            dict or list: The response content in JSON format, or an empty
            dictionary or list if there is no content.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        url: str = f'{self.__base_url}{req.url}'
        resp = requests.get(url=url, json=req.params, headers=self.__headers)
        # Return the result
        return resp

    @handler
    def __post(self, req: Api42Request) -> requests.Response:
        """Sends a POST request and handles the response.

        Args:
            req (Api42Request): The request object.

        Returns:
            dict or list: The response content in JSON format, or an empty
            dictionary or list if there is no content.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        url: str = f'{self.__base_url}{req.url}'
        resp = requests.post(url=url, json=req.data, headers=self.__headers)
        # Return the result
        return resp

    @handler
    def __patch(self, req: Api42Request) -> requests.Response:
        """Sends a PATCH request and handles the response.

        Args:
            req (Api42Request): The request object.

        Returns:
            dict or list: The response content in JSON format, or an empty
            dictionary or list if there is no content.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        url: str = f'{self.__base_url}{req.url}'
        resp = requests.patch(url=url, json=req.data, headers=self.__headers)
        # Return the result
        return resp

    @handler
    def __put(self, req: Api42Request) -> requests.Response:
        """Sends a PUT request and handles the response.

        Args:
            req (Api42Request): The request object.

        Returns:
            dict or list: The response content in JSON format, or an empty
            dictionary or list if there is no content.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        url: str = f'{self.__base_url}{req.url}'
        resp = requests.put(url=url, json=req.data, headers=self.__headers)
        # Return the result
        return resp

    @handler
    def __delete(self, req: Api42Request) -> requests.Response:
        """Sends a DELETE request and handles the response.

        Args:
            req (Api42Request): The request object.

        Returns:
            dict or list: The response content in JSON format, or an empty
            dictionary or list if there is no content.

        Raises:
            Api42RequestError: If an error occurs while making the request and
                `self.__raises` is set to True.
        """
        # Making the request
        url: str = f'{self.__base_url}{req.url}'
        resp = requests.delete(url=url, json=req.data, headers=self.__headers)
        # Return the result
        return resp
