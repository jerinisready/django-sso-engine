
# if Django"
from flask_view.conf import settings
from flask_view.contrib import messages
from flask_view.contrib.auth import authenticate, login
from flask_view.http import JsonResponse
from flask_view.shortcuts import redirect, render
from contrib.clients.python.service import SSOAgent


def login_page(request):
    cxt = {
        'sso_authentication_route': SSOAgent(settings.DJ_SSO_API_KEY).authentication_route
    }
    return render(request, 'index.html', cxt)


def sso_callback(request):
    if request.GET.get('state') != 'SUCCESS':
        messages.info(request, 'SSO Authentication Failed!')
        return redirect('login')
    sso = SSOAgent(settings.DJ_SSO_API_KEY, token=request.GET['auth_token'])
    user = authenticate(request, sso_agent=sso)
    if user is None:
        return JsonResponse({'state': sso.response_state}, status=400)
    login(request, user)
    return JsonResponse({'state': sso.response_state}, status=200)


