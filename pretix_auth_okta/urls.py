from django.urls import path

from .views import return_view, start_view

urlpatterns = [
    path('_okta/start', start_view, name='start'),
    path('_okta/return', return_view, name='return'),
]
