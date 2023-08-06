import datetime
import json
import os
import platform
import requests
from typing import Dict, List, Optional

from .__version__ import version
from .auth import OAuth2Handler, fetch_token
from .constants import DEFAULT_DDC_API_URL
from .errors import (BadRequest, DdcException, DdcRequestError, DdcServerError,
                     Forbidden, HTTPException, NotFound, TooManyRequests,
                     Unauthorized)
from .metadata import DanubeDataCubeMetadata


class DdcClient():
    """
    Represents a Danube Data Cube client.

    Args:
        client_id (str): Danube Data Cube client id.
        client_secret (str): Danube Data Cube client secret.
        host (Optional[str] ): Alternative Danube Data Cube host url.
        token (Optional[str]): Alternative Danube Data Cube token API URL.
        trace_store_calls (bool): Whether store calls shall be
            printed (for debugging).

    """

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 host: Optional[str] = DEFAULT_DDC_API_URL,
                 token: Optional[str] = None,
                 trace_store_calls: bool = False) -> None:

        client_id = client_id or os.environ.get('DDC_CLIENT_ID')
        client_secret = client_secret or os.environ.get(
            'DDC_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise ValueError(
                'Both "client_id" and "client_secret" must be provided. '
                'Consider setting environment variables '
                'DDC_CLIENT_ID and DDC_CLIENT_SECRET.'
            )

        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.host = host

        self.auth = None
        self.session = requests.Session()
        self.user_agent = (
            f"Python/{platform.python_version()} "
            f"Requests/{requests.__version__} "
            f"ddc_cube/{version}"
        )
        self._trace_store_calls = trace_store_calls

    def request(self, method: str, route: str, params: Optional[Dict] = None,
                json_data: Optional[Dict] = None, mime_type: str = 'application/json'):

        headers = {
            "Accept": mime_type,
            "User-Agent": self.user_agent,
            "client_id": self.client_id
        }

        url = self.host + route

        self._set_auth_handler()
        auth = self.auth.apply_auth()

        if self._trace_store_calls:
            print(
                f"Making API request: {method} {url}\n"
                f"Parameters: {params}\n"
                f"Headers: {headers}\n"
                f"Body: {json_data}"
            )

        with self.session.request(
                method, url, params=params, json=json_data, headers=headers,
                auth=auth) as response:

            if self._trace_store_calls:
                print(
                    "Received API response: "
                    f"{response.status_code} {response.reason}\n"
                    f"Headers: {response.headers}\n"
                    f"Content: {response.content}"
                )

            if response.status_code == 400:
                raise BadRequest(response)
            if response.status_code == 401:
                raise Unauthorized(response)
            if response.status_code == 403:
                raise Forbidden(response)
            if response.status_code == 404:
                raise NotFound(response)
            if response.status_code == 429:
                raise TooManyRequests(response)
            if response.status_code >= 500:
                raise DdcServerError(response)
            if not 200 <= response.status_code < 300:
                raise HTTPException(response)

            return response

    def _set_auth_handler(self):

        if self.token:
            auth = OAuth2Handler(self.token)

            if self._trace_store_calls:
                print("Token provided manually, "
                      "didn't make a request to fetch token.")
        else:
            now = datetime.datetime.now()
            if self.auth is None or (self.auth.expires_at - now).total_seconds() < 30:
                token_url = self.host + '/dynamic_data_cube/get_token'
                headers = {
                    "Accept": 'application/json',
                    "User-Agent": self.user_agent,
                    "client_id": self.client_id
                }
                auth_data = {'client_id': self.client_id,
                             'client_secret': self.client_secret}

                token = fetch_token(auth_data, headers, token_url)
                auth = OAuth2Handler(
                    token.get('bearer_token'), token.get('expires_at'))

                if self._trace_store_calls:
                    print(
                        f"Making API request: 'POST' {token_url}\n"
                        f"Parameters: {None}\n"
                        f"Headers: {headers}\n"
                        f"Body: {'client_id': self.client_id, 'client_secret': '*****'}"
                    )
                    print("Token is not provided or expired, made a request to fetch token.")
            else:
                auth = self.auth

                if self._trace_store_calls:
                    print(
                        "Token provided through auth object , "
                        "didn't make a request to fetch token.")

        self.auth = auth


class DanubeDataCube():
    """Represents the Danube Data Cube data portal.

    Args:
        client_id (Optional[str]): Danube Data Cube client id.
        client_secret (Optional[str]): Danube Data Cube client secret.
        token (Optional[str]): Alternative Danube Data Cube token API URL.
        client (Optional[DdcClient]): Danube Data Cube Client instance.

    Examples:
        # Create an DanubeDataCube object
        >>> DDC = DanubeDataCube(<client_id>, <client_secret>)
        # List the available DDC Environmental dataset
        >>> DDC.dataset_names
        # List the user's Custom datasets available through the DDC AOI Manager
        >>> DDC.get_aoi()

    """

    METADATA = DanubeDataCubeMetadata()

    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token: Optional[str] = None,
                 client: Optional[DdcClient] = None):

        # Client credentials
        if client is None:
            client_id = client_id or os.environ.get('DDC_CLIENT_ID')
            client_secret = client_secret or os.environ.get(
                'DDC_CLIENT_SECRET')

            client = DdcClient(client_id, client_secret, token=token)

        self.client = client

    @ property
    def datasets(self) -> Dict:
        """Datasets available in Danube Data Cube."""
        return self.METADATA.datasets

    @ property
    def dataset_names(self) -> List[str]:
        """Names of the datasets available in Danube Data Cube."""
        return self.METADATA.dataset_names

    def dataset(self, dataset_name: str) -> Optional[Dict]:
        """
        Dataset specified by the name.

        Args:
            dataset_name (str): Name of the dataset.
        """
        return self.METADATA.dataset(dataset_name)

    def dataset_vars(self, dataset_name: str, default=None) -> Optional[Dict]:
        """Variables available specified by the dataset name.

        Args:
            dataset_name (str): Name of the dataset.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_vars(dataset_name, default)

    def dataset_vars_names(self, dataset_name: str,
                           default=None) -> Optional[List[str]]:
        """Names of the variables available specified by the dataset name.

        Args:
            dataset_name (str): Name of the dataset.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_vars_names(dataset_name, default)

    def dataset_var(self, dataset_name: str, variable_name: str,
                    default=None) -> Optional[Dict]:
        """Variable specified by the dataset name and variable name.

        Args:
            dataset_name (str): Name of the dataset.
            variable_name (str): Name of the variable.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_var(dataset_name, variable_name, default)

    def get_aoi(self, with_geometry: bool = True) -> List[Dict]:
        """
        Get user's area of interest (AOI).

        Args:
            with_geometry (bool, optional): Whether to retrive geomatry values.
                Defaults to True.
        """

        params = {'user_id': self.client.client_id,
                  'with_geometry': with_geometry}

        try:
            response = self.client.request(method='get',
                                           route='/aoi_manager/get_aoi',
                                           params=params)
        except HTTPException as error:
            raise DdcException(
                f'Error during getting aoi of the user {self.client.client_id} '
                f'from {"/aoi_manager/get_aoi"}'
            ) from error

        data = json.loads(response.content)

        return data

    def get_properties(self,
                       dataset_name: str) -> Dict:
        """
        Get the properties of the dataset e.g. geographical and temporal
        extent, resolution, datatype etc..

        Args:
            dataset_name (str): Name of the dataset.
        """

        params = {'dataset': dataset_name.lower()}

        try:
            response = self.client.request(method='get',
                                           route='/dynamic_data_cube/get_meta',
                                           params=params)
        except HTTPException as error:
            raise DdcException(
                f'Error during getting properties of the dataset {dataset_name} '
                f'from the endpoint of {"/dynamic_data_cube/get_meta"}'
            ) from error

        data = json.loads(response.content)

        return data

    def get_custom_properties(self,
                              dataset_name: str) -> Dict:
        """
        Get the properties of user's custom zarr datset e.g. geographical and temporal
        extent, resolution, datatype etc..

        Args:
            dataset_name (str): Name of the custom zarr.
        """

        params = {'dataset': dataset_name.lower()}

        try:
            response = self.client.request(method='get',
                                           route='/dynamic_data_cube/get_custom_meta',
                                           params=params)
        except HTTPException as error:
            raise DdcException(
                f'Error during getting properties of the dataset {dataset_name} '
                f'from the endpoint of {"/dynamic_data_cube/get_custom_meta"}'
            ) from error

        data = json.loads(response.content)

        return data

    def get_data(self, route: str, request: Dict) -> Dict:
        """
        Fetch data from backend.

        Args:
            dataset_name (str): Name of the dataset.
            mime_type (str): Media type, default is 'application/json'.
        """

        try:
            response = self.client.request(
                method='get', route=route,
                params=request, mime_type='application/octet')
        except HTTPException as error:
            raise DdcRequestError(
                f'Error during getting data, with parameters of {request} '
                f'from the endpoint of {route}'
            ) from error

        return response
