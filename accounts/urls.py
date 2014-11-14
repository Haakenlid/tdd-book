from django.conf.urls import url, patterns
from .views import persona_login

urlpatterns = patterns(
    '',
    url(r'^login$', persona_login, name='persona_login',),
)
