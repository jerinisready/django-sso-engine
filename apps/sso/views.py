from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from django.views.generic.edit import ProcessFormView, ModelFormMixin, UpdateView

from apps.sso.facade import SSOService
from apps.sso.models import Client, AuthTransaction, AccessAgreement


# Create your views here
class WebSSO(ModelFormMixin, LoginView, ProcessFormView, ):

    form_class = AuthenticationForm
    template_name = 'sso/web-login.html'

    def get_object(self, queryset=None):
        return Client.get_with_key(self.request.GET['apikey'])

    def invalid_api_key(self):
        return render(self.request, 'sso/invalid_vendor_configuration.html')

    def get_context_data(self, **kwargs):
        cxt = super().get_context_data(**kwargs)
        cxt['client'] = self.client
        return cxt

    def get(self, request, *args, **kwargs):
        """
        Usually, other system allows authentication, even when we donot have a client, and will redirect to native dashboard.
        Since we are concentrating only on authentication service, we
        """
        if 'apikey' not in request.GET:
            return self.invalid_api_key()
        self.client = self.get_object()
        if self.request.user.is_authenticated:
            return self.next_level(user=self.request.user, has_already_completed=True)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Usually, other system allows authentication, even when we donot have a client, and will redirect to native dashboard.
        Since we are concentrating only on authentication service, we
        """
        if 'apikey' not in request.GET:
            return self.invalid_api_key()
        self.client = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return redirect(self.next_level(form.get_user()))

    def next_level(self, user, has_already_completed=False):
        service = SSOService()
        state = (
            AuthTransaction.AUTH_ALREADY_LOGIN
            if has_already_completed else AuthTransaction.AUTH_LOGIN
        )
        service.generate_transaction(client=self.client, user=user, state=state)
        return service.next_route()


class WebSSOPermissionUpdateView(UpdateView):
    model = AccessAgreement
    fields = ('permissions', )

    def get_object(self, queryset=None):
        return self.service.txn.agreement

    def get(self, request, *args, **kwargs):
        self.service = SSOService(**kwargs)
        if self.service.txn.is_signed is True:
            """
            Transaction signed means, the user is already updated the permissions on his will.
            """
            return redirect(self.next_level(has_already_completed=True))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.service.sign_agreement()           # sign when user updates permissions first time.
        return redirect(self.next_level())

    def next_level(self, has_already_completed=False):
        new_state = (
            AuthTransaction.ALREADY_HAVE_PERMISSION
            if has_already_completed
            else AuthTransaction.SETTING_PERMISSIONS
        )
        self.service.set_state(new_state)
        return self.service.next_route()


class WebSSORedirectView(RedirectView):

    def get(self, request, *args, **kwargs):
        self.service = SSOService(**kwargs)
        self.service.set_state(AuthTransaction.RESPONSE_READY)
        return redirect(self.get_redirect_url())

    def get_redirect_url(self, *args, **kwargs):
        return self.service.redirection_url()





