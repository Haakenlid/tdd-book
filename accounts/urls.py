from django.conf.urls import url, patterns
from .views import persona_login
from django.contrib.auth.views import logout

urlpatterns = patterns(
    '',
    url(r'^login$', persona_login, name='persona_login',),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout',),
)
