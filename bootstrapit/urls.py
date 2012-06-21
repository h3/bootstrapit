from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from bootstrapit.views import *

urlpatterns=patterns('',
    
    url(r'^$', DesignView.as_view(), name='bootstrapit-index'),

    url(r'^edit/(?P<theme>[\d\w-]+)$', 
        login_required(EditorView.as_view()), name='bootstrapit-editor'),

    url(r'^api/editor/$', login_required(EditorBackend.as_view()),
        name='bootstrapit-backend'),

   #url(r'all$',          HomeView.as_view(),     name='bootstrapit-home'),
   #url(r'^editor/recive$', EditorReciveAjax.as_view(), name='bootstrapit-editor-recive'),
   #url(r'^v/(?P<slug>[\d\w-]+)$',  Version.as_view(),      name="bootstrapversion-home"),
   #url(r'^v/(?P<slug>[\d\w-]+)/json$$',  JsonVersion.as_view(),      name="bootstrapversion-json"),
)
