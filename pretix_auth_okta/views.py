import logging
from urllib.parse import quote

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from pretix.base.models import User
from pretix.control.views.auth import process_login
from pretix.helpers.urls import build_absolute_uri

logger = logging.getLogger(__name__)


def start_view(request):
    request.session['pretix_auth_okta_nonce'] = get_random_string(32)
    url = (
            settings.CONFIG_FILE.get('pretix_auth_okta', 'url') +
            '/v1/authorize?client_id={client_id}&none={nonce}&redirect_uri={redirect_uri}&state={state}&response_type=code&response_mode=query&scope=openid+profile+email'
    ).format(
        client_id=settings.CONFIG_FILE.get('pretix_auth_okta', 'client_id'),
        nonce=request.session['pretix_auth_okta_nonce'],
        state=request.session['pretix_auth_okta_nonce'],
        redirect_uri=quote(build_absolute_uri('plugins:pretix_auth_okta:return'))
    )
    return redirect(url)


def return_view(request):
    # check for error state
    if 'error' in request.GET:
        logger.warning('Okta login failed. Response: ' + request.META['QUERY_STRING'])
        messages.error(request, _('Login was not successful. Error: {message}').format(message=request.GET.get('error_description')))
        return redirect(reverse('control:auth.login'))

    try:
        r = requests.post(
            settings.CONFIG_FILE.get('pretix_auth_okta', 'url') + '/v1/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': settings.CONFIG_FILE.get('pretix_auth_okta', 'client_id'),
                'client_secret': settings.CONFIG_FILE.get('pretix_auth_okta', 'client_secret'),
                'redirect_uri': build_absolute_uri('plugins:pretix_auth_okta:return'),
                'code': request.GET.get('code')
            }
        )
        r.raise_for_status()
        response = r.json()
        access_token = response['access_token']

        r = requests.get(
            settings.CONFIG_FILE.get('pretix_auth_okta', 'url') + '/v1/userinfo',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        r.raise_for_status()
        response = r.json()
    except:
        logger.exception('Okta login failed.')
        messages.error(request, _('Login was not successful due to a technical error.'))
        return redirect(reverse('control:auth.login'))

    u, created = User.objects.get_or_create(
        email=response['email'],
        defaults={
            'fullname': '{} {}'.format(
                response.get('given_name', ''),
                response.get('family_name', ''),
            ),
            'locale': response.get('locale').lower()[:2],
            'timezone': response.get('zoneinfo', 'UTC'),
            'auth_backend': 'okta'
        }
    )
    return process_login(request, u, keep_logged_in=False)
