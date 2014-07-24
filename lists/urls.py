from django.conf.urls import patterns, url
from .views import add_item, new_list, view_list

urlpatterns = patterns(
    '',
    url(r'^new$', new_list, name='new_list'),
    url(r'^(\d+)/$', view_list, name='view_list'),
    url(r'^(\d+)/add_item$', add_item, name='add_item'),
)