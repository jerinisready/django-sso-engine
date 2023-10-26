from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.sso.models import AuthTransaction


def resp_structure(state, txn_date, txn_id) -> dict:
    return {
        'state': state,
        'auth': None,
        'txn_date': txn_date if txn_date else None,
        'txn_id': txn_id,
    }


def call_or_draw(user, feature):
    pointer = getattr(user, feature, None)
    if callable(pointer):
        pointer = callable(pointer)
    return pointer

class ResponseSerializer(object):

    def __init__(self, instance, client, txn_id=None):
        self.txn: AuthTransaction = instance
        self.txn_id = txn_id
        self.client = client

    def get_status(self):
        if self.client is None:
            return 'INVALID_CREDENTIALS'
        elif self.txn is None:
            return 'INVALID_ID'
        elif self.txn.agreement.client != self.client:
            return 'UNAUTHORIZED_TXN'
        elif self.txn.created_at < timezone.now() - timedelta(**settings.SSO_AUTH_TIMEOUT):
            return 'EXPIRED'
        elif self.txn.state == AuthTransaction.RESPONSE_READY:
            return 'VERIFIED'
        else:
            return 'INCOMPLETE'

    @property
    def status_code(self):
        return {
            'VERIFIED': 200,
            'INVALID_ID': 400,
            'INVALID_CREDENTIALS': 401,
            'UNAUTHORIZED_TXN': 403,
            'EXPIRED': 410,
            'INCOMPLETE': 418,
        }[self.get_status()]


    @property
    def data(self):
        # VERIFIED, EXPIRED, INCOMPLETE, INVALID_ID, UNAUTHORIZED, INVALID_CREDENTIALS
        state = self.get_status()
        return getattr(self, f'get_{state.lower()}_response')()

    def get_invalid_credentials_response(self):
        r = resp_structure('INVALID_CREDENTIALS', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        return r

    def get_invalid_id_response(self):
        r = resp_structure('INVALID_ID', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        return r

    def get_unauthorized_txn_response(self):
        r = resp_structure('UNAUTHORIZED_TXN', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        return r

    def get_expired_response(self):
        r = resp_structure('EXPIRED', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        return r

    def get_verified_response(self):
        r: dict = resp_structure('VERIFIED', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        features = self.txn.get_permissions()
        r['auth'] = {
            'permitted_features': list(features),
            'features': {feature: call_or_draw(self.txn.agreement.user, feature) for feature in features}
        }
        return r

    def get_incomplete_response(self):
        r = resp_structure('INCOMPLETE', txn_id=self.txn_id, txn_date=self.txn and self.txn.created_at)
        return r
