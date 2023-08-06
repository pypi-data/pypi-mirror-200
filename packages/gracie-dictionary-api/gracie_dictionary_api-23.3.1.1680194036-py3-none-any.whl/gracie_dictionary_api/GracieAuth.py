server_type = 'dictionary'

server_type = 'feeds'

import requests
import time


class GracieKeycloakAuthError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class GracieKeycloakAuth(requests.Session):
    _keycloak_server = None
    _session_information = None
    _login_name = None
    _login_password = None
    _verify_ssl = None
    _grant_type = 'password'
    _client_id = 'api-client'
    _client_secret = 'yxmZymjyMufQgbeNOXvLHv68JOsbaog1'

    def __init__(self, keycloak_host, login_name, login_password, verify_ssl):
        super(GracieKeycloakAuth, self).__init__()
        self._keycloak_server = '%s/auth/realms/NuixNLP/protocol/openid-connect/token' % keycloak_host
        self._login_name = login_name
        self._login_password = login_password
        self._verify_ssl = verify_ssl

    def login(self, login_name=None, login_password=None):
        if not login_name:
            login_name = self._login_name
        if not login_password:
            login_password = self._login_password

        payload = {'username': login_name,
                   'password': login_password,
                   'grant_type': self._grant_type,
                   'client_id': self._client_id,
                   'client_secret': self._client_secret}
        response = self.post(self._keycloak_server, data=payload, verify=self._verify_ssl)
        if response.status_code != 200:
            raise GracieKeycloakAuthError(
                '%s error authenticating to Keycloak server: %s' % (response.status_code, response.text))
        self._session_information = response.json()
        self._session_information['expire_time'] = self._session_information['expires_in'] + int(time.time())
        return response.status_code

    @property
    def access_token(self):
        return self.access_info['access_token']

    @property
    def access_info(self):
        # if session is not set or the token has expired login
        if not self._session_information or ('expire_time' in self._session_information and (
                self._session_information['expire_time'] - int(time.time()) <= 60)):
            self.login(self._login_name, self._login_password)
        return self._session_information

    @property
    def access_headers(self):
        return {'authorization': '%s %s' % (self.access_info['token_type'].capitalize(),
                                            self.access_info['access_token'])}
