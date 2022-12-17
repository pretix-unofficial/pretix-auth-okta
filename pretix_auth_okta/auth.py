from django.conf import settings
from django.urls import reverse
from pretix.base.auth import BaseAuthBackend
from urllib.parse import quote


class OktaAuthBackend(BaseAuthBackend):
    identifier = "okta"

    @property
    def verbose_name(self):
        return settings.CONFIG_FILE.get('pretix_auth_okta', 'label', fallback='Okta')

    def authentication_url(self, request):
        u = reverse('plugins:pretix_auth_okta:start')
        if 'next' in request.GET:
            u += '?next=' + quote(request.GET.get('next'))
        return u

    def get_next_url(self, request):
        if hasattr(request, '_okta_next'):
            return request._okta_next
