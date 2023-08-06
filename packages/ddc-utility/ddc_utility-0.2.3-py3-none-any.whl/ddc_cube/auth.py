import datetime
from typing import Dict

import requests

from .errors import DdcException, DdcServerError, HTTPException


def fetch_token(auth_data: Dict, headers: Dict, token_url: str
) -> Dict:
    """Feetch token from a remote token endpoint.

    Args:
        auth_data (Dict): Dictionary holding 'client_id' and 'client_secret'.
        headers (Dict): Request headers.
        token_url (str): Token endpoint url.
    """

    now = datetime.datetime.now()
    with requests.post(token_url, headers=headers, json=auth_data,
                       timeout=10) as response:

        if response.status_code >= 500:
            raise DdcServerError(response)
        if not 200 <= response.status_code < 300:
            raise HTTPException(response)
        if b"Error" in response.content:
            raise HTTPException(response)

        data = response.json()

    if data.get('token_type').lower() != 'bearer':
        raise DdcException('Expected token_type to equal "bearer", '
                           f'but got {data.get("token_type")} instead')

    expires_at = now + datetime.timedelta(seconds=data.get('expires_in'))
    bearer_token = data['access_token']

    return {'bearer_token': bearer_token,
            'expires_at': expires_at}


class OAuth2Handler:

    def __init__(self, bearer_token: str, expires_at=None):

        self.bearer_token = bearer_token
        self.expires_at = expires_at

    def apply_auth(self):
        return OAuth2BearerHandler(bearer_token=self.bearer_token)


class OAuth2BearerHandler(requests.auth.AuthBase):
    """OAuth 2.0 Bearer Token authentication handler"""

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def __call__(self, request: requests.Request):
        request.headers['Authorization'] = 'Bearer ' + self.bearer_token
        return request
