import configparser
import json
import requests
from utradeconnect.exception import UtradeDataException, UtradeGeneralException, UtradeTokenException
from utradeconnect.apiConfig import get_all_routes


class ConfigReader:
    def __init__(self):
        """
        Initializes the ConfigReader object by reading the provided config file path.
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_user_source(self):
        """
        Retrieves the 'source' value from the [user] section of the config file.

        Returns:
            str: The 'source' value.
        """
        return self.config.get('user', 'source')

    def is_ssl_disabled(self):
        """
        Checks if SSL is disabled.

        Returns:
            bool: True if SSL is disabled, False otherwise.
        """
        return self.config.getboolean('SSL', 'disable_ssl')

    def get_root_url(self):
        """
        Retrieves the 'root' value from the [root_url] section of the config file.

        Returns:
            str: The 'root' value.
        """
        return self.config.get('root_url', 'root')

    def get_broadcast_mode(self):
        """
        Retrieves the 'broadcastMode' value from the [root_url] section of the config file.

        Returns:
            str: The 'broadcastMode' value.
        """
        return self.config.get('root_url', 'broadcastMode')


def _unwrap_envelope(data):
    """Unwrap a one-element market-data array envelope into a dict.

    Converter market-data success bodies are often
    [{type, code, description, result}]. Interactive bodies are already a dict.
    Nested ``result`` arrays (cancel, quotesList) are left intact.
    """
    if (
        isinstance(data, list)
        and len(data) == 1
        and isinstance(data[0], dict)
        and ("result" in data[0] or "type" in data[0] or "code" in data[0])
    ):
        return data[0]
    return data


def _is_error_envelope(data, status_code):
    if status_code >= 400:
        return True
    if not isinstance(data, dict):
        return False
    if data.get("type") == "error":
        return True
    # Some endpoints report empty results as a success envelope carrying an "e-" code
    # (e.g. e-spread-0002 "No Data Available"), which is not a failure.
    if data.get("type") == "success":
        return False
    if data.get("error"):
        return True
    code = data.get("code")
    if isinstance(code, str) and code.startswith("e-"):
        return True
    return False


def _api_error_message(data):
    if isinstance(data, dict):
        description = data.get("description")
        if description:
            return description
        error = data.get("error")
        if error and error is not True:
            return str(error)
    return str(data)


def _raise_api_error(data, status_code):
    code = None
    if isinstance(data, dict):
        code = data.get("code")
    message = _api_error_message(data)
    if status_code == 401 or (isinstance(code, str) and str(code).startswith("e-auth")):
        raise UtradeTokenException(message, status_code)
    raise UtradeGeneralException(message, status_code)


class APIRequest:
    """
    Represents an API request.

    Args:
        base_url (str, optional): The base URL for the API. Defaults to None.
        token (str, optional): The authorization token. Defaults to None.
        disable_ssl (bool, optional): Whether to disable SSL verification. Defaults to False.
        debug (bool, optional): Whether to enable debug mode. Defaults to False.
        timeout (int, optional): The timeout for the request. Defaults to 100.
    """

    def __init__(self, base_url=None, token=None, disable_ssl=False, debug=False, timeout=100):
        # Initialize the APIRequest with the configuration from the file
        config_reader = ConfigReader()
        self.root = base_url if base_url is not None else config_reader.get_root_url()
        self.token = token
        self.disable_ssl = disable_ssl if disable_ssl is not None else config_reader.is_ssl_disabled()
        self.debug = debug
        self.reqsession = requests
        self.timeout = timeout if timeout is not None else 100
        self._routes = get_all_routes()
        # disable requests SSL warning
        requests.packages.urllib3.disable_warnings()

    def _get(self, route, params=None):
        """
        Alias for sending a GET request.

        Args:
            route (str): The route to send the GET request to.
            params (dict, optional): The parameters to include in the GET request.

        Returns:
            The response from the GET request.
        """
        return self._request(route, "GET", params)

    def _post(self, route, params=None):
        """
        Alias for sending a POST request.

        Args:
            route (str): The route to send the request to.
            params (dict, optional): The parameters to include in the request. Defaults to None.

        Returns:
            The response from the POST request.
        """
        return self._request(route, "POST", params)

    def _put(self, route, params=None):
        """
        Alias for sending a PUT request.

        Args:
            route (str): The route for the PUT request.
            params (dict, optional): The parameters to be sent with the request. Defaults to None.

        Returns:
            The response from the PUT request.
        """
        return self._request(route, "PUT", params)

    def _delete(self, route, params=None):
        """
        Alias for sending a DELETE request.

        Args:
            route (str): The route for the DELETE request.
            params (dict, optional): The parameters to be included in the request.

        Returns:
            The response from the DELETE request.
        """
        return self._request(route, "DELETE", params)

    def _request(self, route, method, parameters=None):
        """Make an HTTP request.

        Args:
            route (str): The route for the request.
            method (str): The HTTP method for the request.
            parameters (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            dict: The response data from the server.

        Raises:
            UtradeDataException: If the server response cannot be parsed as JSON or has an unknown content type.
            UtradeTokenException: If the server response is an auth error.
            UtradeGeneralException: If the server response is a non-auth API error.
        """
        params = parameters if parameters else {}

        uri = self._routes[route]
        root = (self.root or "").rstrip("/")
        url = root + uri

        # The proxy gzips large JSON and re-frames it as chunked, which truncates
        # multi-MB payloads mid-body, so ask for an identity-encoded response.
        headers = {"Content-Type": "application/json", "Accept-Encoding": "identity"}
        if self.token:
            headers["Authorization"] = self.token

        body = None
        query = None
        if method in ["POST", "PUT"]:
            if isinstance(params, dict):
                body = json.dumps(params)
            else:
                body = params
        else:
            query = params if isinstance(params, dict) else None

        try:
            r = self.reqsession.request(
                method,
                url,
                data=body,
                params=query,
                headers=headers,
                verify=not self.disable_ssl,
                timeout=self.timeout,
            )
        except Exception as e:
            raise e

        content_type = (r.headers.get("content-type") or "").lower()
        if "json" in content_type:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise UtradeDataException(
                    "Couldn't parse the JSON response received from the server: {content}".format(
                        content=r.content
                    )
                )
            data = _unwrap_envelope(data)
            if self.debug:
                print(data)
            if _is_error_envelope(data, r.status_code):
                _raise_api_error(data, r.status_code)
            return data

        raise UtradeDataException(
            "Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=r.headers.get("content-type"),
                content=r.content,
            )
        )
