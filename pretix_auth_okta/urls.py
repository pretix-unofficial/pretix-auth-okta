from django.conf.urls import url

from .views import return_view, start_view

urlpatterns = [
    url(r'^_okta/start$', start_view, name='start'),
    url(r'^_okta/return$', return_view, name='return'),
]
