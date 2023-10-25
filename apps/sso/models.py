from django.conf import settings
from django.db import models
from uuid import uuid4

from django.utils import timezone


class Client(models.Model):
    """
    Purpose of this class is to Create credentials for Associated Services.
    If we want to add associated users, or other entities, Feel free to extend this.

    TODO: We need to make app key and app_secret store like password 'django.contrib.auth.hashers.make_password'
    """
    name = models.CharField(max_length=100)
    redirection_url = models.CharField(max_length=500)

    app_key = models.CharField(max_length=200)
    app_secret = models.CharField(max_length=200)

    responsibility_bearer = models.CharField(max_length=200, null=True)
    required_features = models.ManyToManyField('sso.Feature', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        if not self.app_key:
            self.set_keys()
        super().save(**kwargs)

    @classmethod
    def get_with_key(cls, api_key, app_secret=None):
        qs = cls.objects.filter(api_key=api_key)
        if app_secret:
            qs = qs.filter(app_secret=app_secret)
        return qs.first()

    def set_keys(self):
        if self.app_key:
            self.app_key = "key_" + str(uuid4())
        if not self.app_secret:
            self.app_secret = "secret_"+ str(uuid4())


STATE_CHOICES = [
    (1, 'AUTH_REQ'),
    (2, 'AUTH_LOGIN'),
    (3, 'AUTH_ALREADY_LOGIN'),
    (4, 'SETTING_PERMISSIONS'),
    (5, 'ALREADY_HAVE_PERMISSION'),
    (6, 'RESPONSE_READY'),
]


class Feature(models.Model):
    """
    Feature model stores each feature code and a name.
    """
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.code


class AccessAgreement(models.Model):
    """
    Access Agreement Model mocks up the agreement between user and the client.
    This also act as the list of features required by the client.

    Create an instance, only with user's permission in UI.

    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(Feature, blank=True)

    # TIMESTAMPS
    signed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'user',)


class AuthTransaction(models.Model):
    """
    When each transaction,
    """
    AUTH_REQ = 1
    AUTH_LOGIN = 2
    AUTH_ALREADY_LOGIN = 3
    SETTING_PERMISSIONS = 4
    ALREADY_HAVE_PERMISSION = 5
    RESPONSE_READY = 6

    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=1)
    agreement = models.ForeignKey(AccessAgreement, null=True, blank=True, on_delete=models.SET_NULL,)
    txn_token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, **kwargs):
        if not self.txn_token:
            self.generate_token()
        super().save(**kwargs)

    def generate_token(self):
        self.txn_token = "txn_" + str(uuid4())[:16]

    def set_state(self, to_state):
        if to_state in settings.SSO_STATE_TRANSACTIONS[self.state]:
            cp = self.state
            self.state = to_state
            self.set_log(cp, self.state)
            self.save()
        else:
            a = settings.SSO_STATE_LABELS[self.state]
            b = settings.SSO_STATE_LABELS[to_state]
            term_directly = ('directly' if self.state < to_state else '')
            raise Exception(f"Invalid transaction: Could not update from {a} to {b} {term_directly}")

    def set_log(self, prev, curr):
        AuthTransactionLog.objects.create(txn=self, prev=prev, curr=curr)

    def get_permissions(self):
        if self.agreement_id:
            return self.agreement.permissions.all().values_list('code', flat=True)
        return []

    @classmethod
    def generate_txn(cls, client, user=None, state=AUTH_REQ):
        agreement, _is_created = AccessAgreement.objects.get_or_create(client=client, user=user)
        self = cls(user=user, state=state, agreement=agreement)
        self.save()
        return self

    def sign(self):
        self.is_signed = True
        self.signed_at = timezone.utils.now()
        self.save()


class AuthTransactionLog(models.Model):
    txn = models.ForeignKey(AuthTransaction, on_delete=models.CASCADE)
    prev = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    curr = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


