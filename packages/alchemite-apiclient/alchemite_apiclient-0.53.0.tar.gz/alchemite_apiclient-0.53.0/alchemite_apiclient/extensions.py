import json
import os
import logging
import time
import ssl
import itertools
import warnings
import webbrowser
from getpass import getpass
from http.server import BaseHTTPRequestHandler, HTTPServer

import tqdm
from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient, \
    OAuth2Error, WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests_oauthlib import OAuth2Session
from requests.adapters import HTTPAdapter

import alchemite_apiclient as client

TOKEN_FILE = ".alchemite_token"

try:
    from urllib3.contrib import pyopenssl

    # Requests v2.23.0 calls pyopenssl.inject_into_urllib3() to "Monkey-patch
    # urllib3 with PyOpenSSL-backed SSL-support" but this causes SSL verification
    # to fail if ca_certs=None passed to urllib3.  In a future version of requests
    # this monkeypatching will only be done if the built-in python SSL module is
    # unavailable or there is no SNI support (https://github.com/psf/requests/pull/5443)
    pyopenssl.extract_from_urllib3()
except ImportError:
    pass


class SystemSSLContextAdapter(HTTPAdapter):
    """
    By default requests uses the SSL CA bundle installed by certifi or, failing
    that, it's own default CA bundle.  We want to use the system CA bundle
    instead.

    One use case for this is where corporate security systems force internet
    connections through a proxy which substitutes SSL certificates with those
    centrally signed by the corporation.  The system CA bundle is updated to
    include the corporate CA but a public CA bundle will not include this.
    """

    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        kwargs["ssl_context"] = context
        context.load_default_certs()
        return super(SystemSSLContextAdapter, self).init_poolmanager(
            *args, **kwargs
        )


auth_redirect_page = """
<html>
<head>
<title>Auth</title>
</head>
<body>
<p>Authorisation successful. You can now close this tab.</p>
<script>
setTimeout(function(){window.close()}, 500);
</script>
</body>
</html>
"""


class Configuration(client.Configuration):
    def __init__(self):
        self.grant_type = ""
        self.client_id = ""
        self.client_secret = ""
        self.username = ""
        self.password = ""
        self.token = {}
        self._session = None
        self._offline_token = None
        self.offline = False

        super(Configuration, self).__init__()

    @property
    def token_endpoint(self):
        return self.host + "/auth/realms/master/protocol/openid-connect/token"

    @property
    def auth_endpoint(self):
        return self.host + "/auth/realms/master/protocol/openid-connect/auth"

    def token_expired(self):
        return self.token["expires_at"] - time.time() < 10

    @property
    def session(self):
        if self._session is None:
            if self.grant_type == "client_credentials":
                client = BackendApplicationClient(client_id=self.client_id)
            elif self.grant_type == "password":
                client = LegacyApplicationClient(client_id=self.client_id)
            elif self.grant_type == "authorization_code":
                client = WebApplicationClient(client_id=self.client_id)
            else:
                raise NotImplementedError(
                    "Unsupported grant_type: %s" % self.grant_type
                )
            self._session = OAuth2Session(client=client)
            adapter = SystemSSLContextAdapter()
            self._session.mount(self.host, adapter)

        return self._session

    def get_token(self):
        try:
            if self.try_offline():
                return self.token

            if self.grant_type == "client_credentials":
                token = self._get_token_client()
            elif self.grant_type == "password":
                token = self._get_token_password()
            elif self.grant_type == "authorization_code":
                token = self._get_token_authorisation()
            else:
                raise NotImplementedError(
                    "Unsupported grant_type: %s" % self.grant_type
                )

            self.save_offline(token)
            return token
        except CustomOAuth2Error as e:
            if self.offline:
                raise ValueError(
                    "Error authenticating. Perhaps Offline Access not enabled for user, please disable and try again") from e
            else:
                raise e

    def _get_token_client(self):
        return self.session.fetch_token(
            token_url=self.token_endpoint,
            client_id=self.client_id,
            client_secret=self.client_secret,
            verify=self.verify_ssl,
        )

    def _get_token_password(self):
        if self.username == "":
            username = input("Please enter Alchemite username: ")
        else:
            username = self.username

        if self.password == "":
            password = getpass("Please enter Alchemite password: ")
        else:
            password = self.password

        token = self.session.fetch_token(
            token_url=self.token_endpoint,
            client_id=self.client_id,
            username=username,
            password=password,
            verify=self.verify_ssl,
        )
        return token

    def _get_token_authorisation(self):
        """
        Performs oauth standard/authorisation_code flow by launching local
        browser.
        The user will be prompted to login through keycloak, and then the token
        is sent back via a temporary http server opened on port 8497 to avoid
        asking people to copy and paste urls.
        """
        authorization_url, state = self.session.authorization_url(
            self.auth_endpoint)
        authorization_response = []

        class AuthServer(BaseHTTPRequestHandler):
            def do_GET(self):
                # Need to pretend that the local exchange was https,
                # though as its entirely local we use http for the final
                # redirect to avoid cert management
                authorization_response.append(
                    f"https://localhost:8497{self.path}")
                self.send_response_only(200)
                self.end_headers()
                self.wfile.write(auth_redirect_page.encode("utf-8"))

        with HTTPServer(('localhost', 8497), AuthServer) as httpd:
            webbrowser.open_new(f"{authorization_url}")

            while len(authorization_response) == 0:
                print("Please log in with your browser...")
                httpd.handle_request()

        token = self.session.fetch_token(
            token_url=self.token_endpoint,
            authorization_response=authorization_response.pop(),
            client_id=self.client_id,
            verify=self.verify_ssl,
        )

        return token

    def try_offline(self):
        if not self.offline:
            return False
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as file:
                offline_token = file.read()
                self._offline_token = offline_token
                try:
                    self.token["refresh_token"] = offline_token
                    self.refresh_token()
                    return True
                except (ValueError, OAuth2Error):
                    return False

    def save_offline(self, token):
        if not self.offline:
            return
        if token['refresh_token'] == self._offline_token:
            # Nothing to update
            return
        if ('offline_access' in token['scope']
                and token['refresh_expires_in'] == 0):
            self._offline_token = token['refresh_token']
            with open(TOKEN_FILE, 'w') as file:
                file.write(token['refresh_token'])

    def refresh_token(self):
        # Make request with 'grant_type'='refresh_token'
        self.token = self.session.refresh_token(
            token_url=self.token_endpoint,
            client_id=self.client_id,
            refresh_token=self.token["refresh_token"],
            verify=self.verify_ssl,
        )
        self.save_offline(self.token)

    @property
    def access_token(self):
        if not self.token:
            self.token = self.get_token()
        elif self.token_expired():
            # try:
            #     self.refresh_token()
            # except oauthlib.oauth2.rfc6749.errors.InvalidGrantError:
            #     # The refresh token has expired or been revoked
            #     self.token = self.get_token()
            self.token = self.get_token()

        return self.token["access_token"]

    @access_token.setter
    def access_token(self, val):
        self._access_token = val

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, config_json_path):
        """Set attributes from JSON"""
        with open(config_json_path) as file:
            self._credentials = json.load(file)
        for key, val in self._credentials.items():
            setattr(self, key, val)
        if "insecure" in self._credentials and self._credentials["insecure"]:
            logging.getLogger(__name__).error(
                "INSECURE mode enabled. This is strongly not recommended in production"
            )
            logging.getLogger(__name__).error(
                "If you are not Intellegens staff, please remove 'insecure' from your credentials file to avoid potential security risks"
            )
            # Debug shim
            import os
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            self.verify_ssl = False


def await_trained(get_model):
    """
    Block until the model is 'trained' and a print progress bar with updates

    Parameters
    ----------
    get_model : func
        Function which returns the model metadata when called

    Returns
    -------
    Model
        The model metadata after training is completed
    """

    with tqdm.tqdm(total=100, unit="%") as pbar:
        while True:
            model = get_model()
            training_progress = model.training_progress
            hyperopt_progress = model.hyperparameter_optimization_progress
            validation_method = model.validation_method

            if training_progress is None:
                training_progress = 0

            if hyperopt_progress is None:
                hyperopt_progress = 0
                progress = training_progress
            else:
                progress = (60 * hyperopt_progress + training_progress) / 61

            pbar.update(progress - pbar.n)

            pbar.set_description(model.status)
            if (
                    (
                            model.status == "trained"
                            and (
                                    validation_method == "none"
                                    or model.validation_r_squared is not None
                            )
                            and (
                                    model.training_dataset_outliers_job_id is None
                                    or model.training_dataset_outliers_job_status == "done"
                            )
                    )
                    or model.status == "failed"
                    or model.training_dataset_outliers_job_status == "failed"
            ):
                break
            time.sleep(1)

    if model.status != "trained":
        raise RuntimeError(f"Model is not trained, status: {model.status}")

    if model.training_dataset_outliers_job_id is not None:
        assert model.training_dataset_outliers_job_status == "done"
    return model


def await_optimized(get_optimize_job):
    warnings.warn(
        "await_optimized is deprecated, please use await_job instead",
        DeprecationWarning,
    )

    return await_job(get_optimize_job)


def await_job(get_job):
    """
    Block until the optimize job is 'done' and a print progress bar with updates

    Parameters
    ----------
    get_job : func
        Function which returns the optimize job metadata when called

    Returns
    -------
    dict
        The optimize job result with metadata
    """
    status = None
    with tqdm.tqdm(total=100, unit="%") as pbar:
        while True:
            job = get_job()
            status = job["status"]

            if "progress" in job:
                progress = job["progress"]
            elif status == "done":
                progress = 100
            else:
                progress = 0
            pbar.update(progress - pbar.n)

            pbar.set_description(status)
            if status in ["done", "failed"]:
                break
            time.sleep(1)

    if status != "done":
        raise RuntimeError(
            f"Job {job['id']} did not complete successfully: {job['detail']}"
        )

    return job


def row_chunks(file_name, chunk_size=1000):
    """
    Generator which splits file_name into chunks with chunk_size rows each.
    The first row of the file (the column header row) is prepended to the top
    of each chunk.

    Parameters
    ----------
    file_name : str
        Path to file which is to be split into chunks
    chunk_size : int
        How many rows (excluding the column header row) there should be in each
        chunk.  The last chunk may have less than this.

    Yields
    ------
    str
        A chunk of file_name with the column header row prepended to the top of
        each file.
    """
    with open(file_name, "r") as file:
        column_header_row = file.readline()

        while True:
            chunk = list(itertools.islice(file, chunk_size))
            if chunk == []:
                # Reached the end of the file
                break

            yield column_header_row + "".join(chunk)
