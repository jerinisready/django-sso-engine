from django.urls import reverse_lazy
from django.utils import timezone

from apps.sso.models import AuthTransaction


class SSOService(object):
    client = None
    user = None

    def __init__(self, txn_token: str = None):
        if txn_token:
            self.txn = AuthTransaction.objects.filter(txn_token=txn_token).select_related(
                'agreement', 'agreement__client', 'agreement__user', 'agreement__permissions'
            ).first()
            self.client, self.user = self.txn.agreement.client, self.txn.agreement.agreement
            self.permissions = self.txn.get_permissions()
        (self.txn, self.client, self.user, self.permissions) = (None, None, None, [])

    def generate_transaction(self, client, user, state):
        self.txn = AuthTransaction.generate_txn(client=client, user=user, state=state)
        return self.txn

    def set_state(self, state):
        self.txn.set_state(state)

    def next_route(self):
        if self.txn.state == AuthTransaction.AUTH_REQ:
            return reverse_lazy('sso-web')          # confirming logins
        if self.txn.state in (AuthTransaction.AUTH_LOGIN, AuthTransaction.AUTH_ALREADY_LOGIN):
            return reverse_lazy('sso-permission')   # confirming permissions
        if self.txn.state in (AuthTransaction.SETTING_PERMISSIONS, AuthTransaction.AUTH_ALREADY_LOGIN):
            return reverse_lazy('sso-redirect')     # processing redirect

    def redirection_url(self):
        url = self.txn.agreement.client.redirection_url
        completion_state = 'SUCCESS' if self.txn.state == AuthTransaction.RESPONSE_READY else 'TERMINATED'
        return f'{url}?auth_token={self.txn.txn_token}&state={completion_state}'

    def sign_agreement(self):
        self.txn.sign()


