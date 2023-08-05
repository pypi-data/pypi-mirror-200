'''
Object for working with Google Cloud authentication tools.
'''

import json
from base64 import b64decode as b64d
from warnings import warn
from jose import jwt
import requests

from google.auth.exceptions import DefaultCredentialsError
import google.auth.transport.requests as transport_req
from google.oauth2 import id_token, service_account


class HeaderGCP():
    '''
    The class provides features to working with authentication systems that work in GCP for
    access to HTTP endpoints.

    The HeaderGCP work with Identity Access Manager on Identity Aware Proxy and/or on
    direct access to cloud instance (Cloud Run / Functions / etc).

    Args:
        key: The path to a service_account key in JSON format

    Raises:
        DefaultCredentialsError: If was got bad key
    '''

    def __init__(self, key: str | None = None, **kw):

        self.key = None
        if key:
            try:
                with open(key, "r", encoding=kw.get('encoding', 'utf-8')) as key_file:
                    key_info = json.load(key_file)
                    if key_info.get("type") == "service_account":
                        self.key = key_info

            except ValueError as caught_exc:
                raise DefaultCredentialsError(
                    f"The {key} is not valid service account credentials."
                ) from caught_exc

        self.request = transport_req.Request()

    def make_bearer(self, scope: str) -> str:
        '''
        Build a value for authentication header which contains Bearer token.

        Args:
            scope: Where the provided token will be act. For Cloud Run/Functions... it is a
                system URL, for IAP with IAM it is account ID (not email!).

        Returns:
            Bearer token.
        '''

        if self.key:
            cred = service_account.IDTokenCredentials.from_service_account_info(
                self.key,
                target_audience=scope
            )
            cred.refresh(self.request)
            token = cred.token

        else:
            token = id_token.fetch_id_token(self.request, scope)

        return f"Bearer {token}"

    def fill_headers(self, scope: str, current: dict | None = None, replace: bool = True) -> dict:
        '''
        This method is a helper for building the headers.

        Args:

            scope: Where the provided token will be act. For Cloud Run/Functions... it is a
                system URL, for IAP with IAM it is account ID (not email!).

            current: An existed headers needs added Bearer to.

            replace: If True and the current header contains the authentication token then
                replace it.

        Returns:
            _description_
        '''

        token = self.make_bearer(scope)

        header = current or {}
        if ('Authorization' in header or 'authorization' in header) and not replace:
            return header
        if 'Authorization' in header:
            del header['Authorization']

        header['authorization'] = token

        return header

    @classmethod
    def read_auth(
        cls,
        headers: dict,
        audience: str | None = None,
        info: str | None = None
    ) -> dict | None:
        '''
        Decryptor & reader for the authorization header.

        Args:

            headers: The request HTTP headers

            audience: The string used Identity Aware Proxy; this argument needs only for IAP

            info: The additional information that will be added to the warning and/or error messages

        Raises:

            TypeError: If provided the current headed is not dict

            ValueError: If was got header from IAP but argument "audience" is an empty.

        Returns:

            Headers with Bearer token
        '''

        if not isinstance(headers, dict):
            raise TypeError(f'The argument "headers" must be a dict, but was got {type("headers")}')

        if 'Authorization' in headers or 'authorization' in headers:

            header = headers.get('Authorization', None) or headers['authorization']

            try:
                b64_profile = header[7:].split('.')[1]
                profile = b64d(b64_profile + '=' * (-len(b64_profile) % 4))
            except Exception as ex:  # pylint: disable=broad-except
                msg = 'The authorization header content is wrong.'
                msg += f'\n\n{info}\n\n{ex}' if info else '\n\n{ex}'
                warn(msg)

                return None

            return json.loads(profile)

        elif 'X-Goog-IAP-JWT-Assertion' in headers or 'x-goog-iap-jwt-assertion' in headers:

            if audience is None:
                raise ValueError(
                    'The argument "audience" is required if headers contains X-Goog-IAP-JWT-Assertion!'
                )

            header = headers.get('X-Goog-IAP-JWT-Assertion', None) or headers['x-goog-iap-jwt-assertion']
            if header is None:   # Request did not come through IAP
                msg = 'X-Goog-IAP-JWT-Assertion header is empty.'
                msg += f'\n\n{info}' if info else ''
                warn(msg)

                return None

            jwt_data = jwt.decode(
                header,
                requests.get('https://www.gstatic.com/iap/verify/public_key', timeout=5).json(),
                algorithms=['ES256'],
                audience=audience
            )

            return jwt_data

        else:
            msg = 'Headers does\'t contains a known authentication headers.'
            msg += f'\n\n{info}' if info else ''
            warn(msg)

            return None

    @classmethod
    def get_user(
        cls,
        headers: dict,
        audience: str | None = None,
        info: str | None = None
    ) -> str | None:
        '''
        The method for get an authenticated user email.

        Args:

            headers: The request HTTP headers.

            audience: The string used Identity Aware Proxy; this argument needs only for IAP

            info: The additional information that will be added to the warning and/or error messages

        Returns:
            Email of authenticated user
        '''

        header = cls.read_auth(headers, audience, info)

        if header and 'email' in header:
            return header['email']

        if header and 'gcip' in header and 'email' in header['gcip']:
            # source https://cloud.google.com/iap/docs/signed-headers-howto#provider_information
            return header['gcip']['email']

        msg = 'Headers is correct but they don\'t contain a known email field.'
        msg += f'\n\n{info}' if info else ''
        warn(msg)

        return None
