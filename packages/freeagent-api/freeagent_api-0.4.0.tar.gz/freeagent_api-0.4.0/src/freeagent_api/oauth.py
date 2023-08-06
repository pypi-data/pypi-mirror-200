"""Module for handling authentication with the FreeAgent API."""
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from requests_oauth2client import AuthorizationRequest, OAuth2Client, BearerTokenSerializer


PRODUCTION_AUTHORIZATION_ENDPOINT = 'https://api.freeagent.com/v2/approve_app'
PRODUCTION_TOKEN_ENDPOINT = 'https://api.freeagent.com/v2/token_endpoint'

SANDBOX_AUTHORIZATION_ENDPOINT = 'https://api.sandbox.freeagent.com/v2/approve_app'
SANDBOX_TOKEN_ENDPOINT = 'https://api.sandbox.freeagent.com/v2/token_endpoint'

AUTH_PORT = 8080
AUTH_RESPONSE_URI = None


class OAuthHandler:
    """Class for handling OAuth tasks.

    Normally you will not need to instantiate this class yourself, as it will be handled by the
    ApiClient class.
    """

    client_id = None
    client_secret = None
    redirect_uri = None

    api_base = None
    authorization_endpoint = None
    token_endpoint = None

    token_serializer = BearerTokenSerializer()
    auth_request = None
    client = None
    bearer_token = None
    is_sandbox: bool = None


    def __init__(self, client_id: str, client_secret: str, use_sandbox: bool = False):
        """Initialise the instance.

        An authentication token will need to be added using do_auth() or loading one from your app's
        storage backend into the serialised_token attribute.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = f"http://localhost:{AUTH_PORT}"
        self.use_sandbox = use_sandbox

        if use_sandbox:
            self.authorization_endpoint = SANDBOX_AUTHORIZATION_ENDPOINT
            self.token_endpoint = SANDBOX_TOKEN_ENDPOINT
        else:
            self.authorization_endpoint = PRODUCTION_AUTHORIZATION_ENDPOINT
            self.token_endpoint = PRODUCTION_TOKEN_ENDPOINT

        self.client = OAuth2Client(
            token_endpoint = self.token_endpoint,
            authorization_endpoint = self.authorization_endpoint,
            auth=(self.client_id, self.client_secret),
        )


    @property
    def serialised_token(self) -> str:
        """Serialise the authentication tokens for storage.

        Returns:
            str: storable tokens
        """
        return self.token_serializer.dumps(self.bearer_token)

    @serialised_token.setter
    def serialised_token(self, value: str):
        self.bearer_token = self.token_serializer.loads(value)
        # Since the serialised token contains the token expiry time at the point the token was
        # serialised, we need to get a new token to update the access token expiry time.
        self.update_tokens(even_if_not_expired=True)


    @property
    def authorisation_header(self) -> str:
        """Return the appropriate string to use in the authentication header in API requests."""
        return self.bearer_token.authorization_header()


    def do_auth(self, only_listen_on_localhost: bool = True):
        """Do the necessary steps to authorise access to the users's account.

        Will open a browser to the login page.

        Args:
            only_listen_on_localhost (bool, optional): Listen to localhost only if true,
                or all interfaces if false. Defaults to True.
        """
        self.auth_request = AuthorizationRequest(
            authorization_endpoint = self.authorization_endpoint,
            client_id = self.client_id,
            redirect_uri = self.redirect_uri,
            scope="age", # FreeAgent's API doesn't use scopes
        )
        print("Opening authorisation page in your browser...")
        print("If this does not work, open the following URL manually:")
        print(self.auth_request.uri)
        webbrowser.open(self.auth_request.uri)

        httpd = HTTPServer(('localhost' if only_listen_on_localhost else '0.0.0.0', AUTH_PORT), _AuthRequestHandler)
        httpd.handle_request()

        #TODO: handle exceptions
        auth_response = self.auth_request.validate_callback(AUTH_RESPONSE_URI)
        self.bearer_token = self.client.authorization_code(auth_response)


    def update_tokens(self, even_if_not_expired: bool = False):
        """Get a new access token if needed. No-op if not.

        Args:
            even_if_not_expired (bool, optional): Get a new token regardless of
                whether it's expired or not. Defaults to False.
        """
        if self.bearer_token:
            if self.bearer_token.is_expired() or even_if_not_expired:
                self.bearer_token = self.client.refresh_token(self.bearer_token.refresh_token)



class _AuthRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)
        params = parse_qs(request.query)
        print(params)

        global AUTH_RESPONSE_URI # pylint: disable=global-statement
        AUTH_RESPONSE_URI = self.path

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("You can close this page now", "utf-8"))
