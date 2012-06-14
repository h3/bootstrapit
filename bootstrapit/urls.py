from django.conf.urls.defaults import *
from django.conf import settings

from bootstrapit.views import *

urlpatterns=patterns('',
    url(r'all$',          HomeView.as_view(),     name='bootstrapit-home'),
    url(r'^v/(?P<slug>[\d\w-]+)',  Version.as_view(),      name="by-version"),
    url(r'', DesignView.as_view(), name='bootstrapit-index'),
)

