from importlib.metadata import version

__version__ = version(__name__)

import concurrent.futures
import json
import logging
import typing
import datetime

import requests

__VALUED_VERSION__ = "0.0.1"


class Connection(object):
    DEFAULT_ENDPOINT = "https://ingest.valued.app/events"

    def __del__(self):
        self._pool.shutdown()

    def __init__(
        self, token: typing.AnyStr, endpoint: typing.AnyStr = DEFAULT_ENDPOINT
    ):
        """Create a Connection class to the Valued endpoint

        Parameters
        ----------
        token : str
            Valued API Token
        endpoint : str, optional
            HTTP endpoint to send the events, default is taken from `DEFAULT_ENDPOINT` value
        """
        self._pool = concurrent.futures.ThreadPoolExecutor()
        self._token = token
        self._endpoint = endpoint

    @property
    def endpoint(self) -> typing.AnyStr:
        """str: Endpoint to send events"""
        return self._endpoint

    @property
    def token(self) -> typing.AnyStr:
        """str: Bearer token for authorization"""
        return self._token

    @property
    def _headers(self) -> typing.Dict:
        """dict: Headers for HTTP requests"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"valued-client/{__VALUED_VERSION__} (Python/{__version__})",
        }

    @staticmethod
    def _call(
        endpoint: typing.AnyStr, headers: typing.Dict, data: typing.Dict
    ) -> typing.Optional[requests.Response]:
        """Posts data to the endpoint with the headers

        This method is what's submitted to the ThreadPoolExecutor and shouldn't
        be called directly

        Parameters
        ----------
        endpoint : str
            Endpoint address to send data
        headers : str
            Headers to pass with the POST
        data : dict
            Data to send in POST

        Returns
        -------
        `requests.Response`, optional
            The response from the API in the event of a success or None

        Examples
        --------
        Sending a call

        >>> con._call("https://localhost:8080", {"Content-Type": "application/json"}, {"highly": "valued"})
        """
        try:
            resp = requests.post(
                endpoint,
                data=json.dumps(data),
                headers=headers,
                timeout=1,
            )
            logging.debug(resp.json())
        except Exception as e:
            logging.error("Exception sending data to ingestion point", exc_info=e)
        return resp

    def send(self, data):
        """Sends data to the valued endpoint

        Parameters
        ----------
        data : dict
            Data to send to the endpoint

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending an action event

        >>> con.send({"category": "action", "id": 123, "email": "support@valued.app" })
        """
        return self._pool.submit(self._call, self.endpoint, self._headers, data)


class Client(object):
    def __init__(self, *args, **kwargs):
        """Class for interacting with Valued

        Parameters
        ----------
        token : str
            Valued API Token
        endpoint : str, optional
            HTTP endpoint to send the events
        """
        self._connection = Connection(*args, **kwargs)

    def action(self, key, data):
        """Send action event for the `key` to Valued

        Parameters
        ----------
        key : str
            Action key in the format `Product.Resource.Action`
            Eg. Portal.Customer.Created
        data : dict
            Attributes for the action

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending an action

        >>> client.action('Portal.Customer.Created', { "customer": { "id": 123, "location": { "country": "NZ" }}})

        Notes
        --------
        https://docs.valued.app/core/event-definitions#action-events
        """
        data["key"] = key
        return self._send_event("action", data)

    def sync(self, data):
        """Send sync event to Valued

        Sync events are used to update the metadata associated with a customer or user

        Parameters
        ----------
        data : dict
            The Customer/User attributes data

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending a sync

        >>> client.sync({ "customer": { "id": 123, "location": { "country": "US" }}})

        Notes
        --------
        https://docs.valued.app/core/event-definitions#sync-events
        """
        return self._send_event("sync", data)

    def sync_customer(self, data):
        """Send customer sync event to Valued

        Parameters
        ----------
        data : dict
            Attributes for the customer

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending a sync

        >>> client.sync_customer({ "id": 123, "location": { "country": "AU" }})

        Notes
        --------
        https://docs.valued.app/core/event-definitions#customer-sync-example
        """
        return self.sync({"customer": data})

    def sync_user(self, data):
        """Send user sync event to Valued

        Parameters
        ----------
        data : dict
            Attributes for the user

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending a sync

        >>> client.sync_user({ "id": 123, "email": "support@valued.app" })

        Notes
        --------
        https://docs.valued.app/core/event-definitions#user-sync-example
        """
        return self.sync({"user": data})

    def _send_event(self, category: typing.AnyStr, data: typing.Dict):
        """Send `data` to Valued with the given `category` type

        Shouldn't be used directly outside of the client

        Parameters
        ----------
        category : str
            Category of the event type
        data : dict
            Data to send to the Valued endpoint

        Returns
        -------
        `concurrent.futures.Future`
            Task associated with sending the event to Valued

        Examples
        --------
        Sending an action event

        >>> client._send_event("action", { "id": 123, "email": "support@valued.app" })
        """
        # TODO: Validate
        data["category"] = category
        if "occured_at" not in data.keys():
            data["occured_at"] = datetime.datetime.now().isoformat()
        return self._connection.send(data)
