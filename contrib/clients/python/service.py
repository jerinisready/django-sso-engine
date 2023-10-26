import requests


class SSOAgent(object):
    ENDPOINT_URL = 'https://sso.example.com'          # endpoint of deployed sso service or http://localhost:8000 for local
    registration_features = ('username', 'email', 'first_name', 'last_name')
    ROUTE = {
        'web': '/sso/web/{api_key}/',
        'verify': '/sso/web/{token}/verify-details/'
    }

    def __init__(self, api_key=None, api_secret=None, endpoint=None, token=None):
        self.SSO_API_KEY = api_key
        self.SSO_API_SECRET = api_secret
        self._response = None
        self.token = token
        self.__resolved = False
        if endpoint:
            self.ENDPOINT_URL = endpoint.rstrip('/')

    @property
    def authentication_route(self):
        return self.ENDPOINT_URL + self.ROUTE['web'].format(api_key=self.SSO_API_KEY)

    @property
    def response(self):
        if self._response is None:
            self._response = self.process_verify_request(self.token)
        return self._response

    @property
    def response_state(self):
        return self.response['body']['state']

    def set_token(self, token):
        self.token = token

    def process_verify_request(self, token):
        """
        API Response will contain these parameters: {'state','auth','txn_date','txn_id'}
            Where auth is optional[dict] which contains these parameters: {permitted_features, features}
            Where features contains the information of the user such as username, email, date_joined e.t.c.
        # state can be one of : VERIFIED, EXPIRED, INCOMPLETE, INVALID_ID, UNAUTHORIZED, INVALID_CREDENTIALS

        """
        url = self.ENDPOINT_URL + self.ROUTE['verify'].format(token=token)
        print("Verifying AT: ", url)
        resp = requests.get(url, headers={
            'X-ApiKey': self.SSO_API_KEY,
            'X-ApiSecret': self.SSO_API_SECRET,
        })
        if resp.status_code >= 500:
            return {'body': {'state': 'INTERNAL_SERVER_ERROR'}, 'auth': None, 'status_code': resp.status_code}
        return {'body': resp.json(), 'status_code': resp.status_code}

    def get_user_details(self):
        """
        This function can be used by normal Python packages and can get the data as return.
        for Django based applications. You can use the SSOAuthenticationMiddleware to process.
        """
        return self.response['body']['auth']

    def get_registration_features(self):
        return self.registration_features
