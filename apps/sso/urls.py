from django.urls import path

from apps.sso.views import WebSSO, WebSSOPermissionUpdateView, WebSSORedirectView


urlpatterns = [
    path('web/<str:apikey>/', WebSSO.as_view(), name="sso-web"),    # login view
    path('web/<str:txn_token>/permission/', WebSSOPermissionUpdateView.as_view(), name="sso-permission"),
    # Confirm Permissions!
    path('web/<str:txn_token>/redirect/', WebSSORedirectView.as_view(), name="sso-redirect"),  # transfer to client site
]
