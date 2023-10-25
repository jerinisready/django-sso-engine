from django.urls import reverse_lazy, reverse
from django.utils import timezone

from apps.sso.models import AuthTransaction
from apps.sso.serializers import ResponseSerializer


class SSOService(object):
    client = None
    user = None

    def __init__(self, txn_token: str = None):
        (self.txn, self.client, self.user, self.permissions) = (None, None, None, [])
        if txn_token:
            self.txn = AuthTransaction.objects.filter(txn_token=txn_token).select_related(
                'agreement', 'agreement__client', 'agreement__user',
            ).first()
            self.client, self.user = self.txn.agreement.client, self.txn.agreement.user
            self.permissions = self.txn.get_permissions()

    def generate_transaction(self, client, user, state):
        self.txn = AuthTransaction.generate_txn(client=client, user=user, state=state)
        return self.txn

    def set_state(self, state):
        self.txn.set_state(state)

    def next_route(self):
        # if self.txn.state == AuthTransaction.AUTH_REQ:
        #     return reverse_lazy('sso-web', txn_token=self.txn.txn_token)          # confirming logins
        if self.txn.state in (AuthTransaction.AUTH_LOGIN, AuthTransaction.AUTH_ALREADY_LOGIN):
            return reverse('sso-permission', kwargs={"txn_token": self.txn.txn_token})   # confirming permissions
        if self.txn.state in (AuthTransaction.SETTING_PERMISSIONS, AuthTransaction.ALREADY_HAVE_PERMISSION):
            return reverse('sso-redirect', kwargs={"txn_token": self.txn.txn_token})     # processing redirect

    def redirection_url(self):
        url = self.txn.agreement.client.redirection_url
        completion_state = 'SUCCESS' if self.txn.state == AuthTransaction.RESPONSE_READY else 'TERMINATED'
        return f'{url}?auth_token={self.txn.txn_token}&state={completion_state}'

    def sign_agreement(self):
        self.txn.agreement.sign()

    def serialize_for_client(self, client, txn_id=None):
        ser = ResponseSerializer(self.txn, client, txn_id=txn_id)
        return ser.data, ser.status_code

