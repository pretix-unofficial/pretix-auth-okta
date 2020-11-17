from django.conf import settings
from django.urls import reverse

from pretix.base.auth import BaseAuthBackend


class OktaAuthBackend(BaseAuthBackend):
    identifier = "okta"

    @property
    def verbose_name(self):
        return settings.CONFIG_FILE.get('pretix_auth_okta', 'label', fallback='Okta')

    def authentication_url(self, request):
        return reverse('plugins:pretix_auth_okta:start')
