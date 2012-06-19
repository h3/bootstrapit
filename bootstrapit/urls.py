from django.conf.urls.defaults import *
from django.conf import settings

from bootstrapit.views import *

urlpatterns=patterns('',
    url(r'all$',          HomeView.as_view(),     name='bootstrapit-home'),
    url(r'^editor$', EditorView.as_view(), name='bootstrapit-editor'),
    url(r'^editor/recive$', EditorReciveAjax.as_view(), name='bootstrapit-editor-recive'),
    url(r'^v/(?P<slug>[\d\w-]+)$',  Version.as_view(),      name="bootstrapversion-home"),
    url(r'^v/(?P<slug>[\d\w-]+)/json$$',  JsonVersion.as_view(),      name="bootstrapversion-json"),
    url(r'^$', DesignView.as_view(), name='bootstrapit-index'),
)
