from django.conf.urls import patterns, url
from .views import new_list, view_list

urlpatterns = patterns(
    '',
    url(r'^new$', new_list, name='new_list'),
    url(r'^(\d+)/$', view_list, name='view_list'),
)