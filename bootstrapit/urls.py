from django.conf.urls.defaults import *
from django.conf import settings

from bootstrapit.views import *


urlpatterns = patterns('',
    url(r'', DesignView.as_view(), name='bootstrapit-index'),
)

