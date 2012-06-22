# -*- coding: utf-8 -*-

from datetime import datetime

from django import http  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import ProcessFormView

from bootstrapit.models import *
from bootstrapit.conf import settings
from bootstrapit.utils import JSONResponseMixin


class EditorView(TemplateView):
    """
    Serves the editor interface (initial load)
    """
    template_name = 'bootstrapit/editor.html'

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        try:
            self.theme = Theme.objects.get(slug=kwargs.get('theme'), 
                            owner_id=self.request.user.pk)
        except Theme.DoesNotExist:
            raise http.Http404

        context['theme'] = self.theme
        context['bootstrap_nav'] = \
                settings.BOOTSTRAPIT_BOOTSTRAP_NAV[\
                self.theme.bootstrap_version]

        context['default_file'] = \
                settings.BOOTSTRAPIT_EDITOR_DEFAULT_FILE
                

        return context


class EditorBackend(ProcessFormView, JSONResponseMixin):
    """
    Handles editor's backend commands
    """
    def post(self, request, *args, **kwargs):
        theme_id = request.POST.get('theme')
        filename = request.POST.get('filename')
        content  = request.POST.get('content')

        if not (content and filename):
            return self.render_to_response({'status':  'error',
                                            'message': 'Missing arguments'})
        try:
            theme = Theme.objects.get(pk=theme_id, owner=request.user) # TODO: OR CONTRIBUOR
        except Theme.DoesNotExist:
            return self.render_to_response({'status':  'error',
                                            'message': 'Theme not found'})

        version = theme.bootstrap_version

        try:
            repos = settings.BOOTSTRAPIT_BOOTSTRAP_VERSIONS[version]
        except:
            return self.render_to_response({'status': 'error',
                    'message' :'Bootstrap version not found',
                    'choices' : settings.BOOTSTRAPIT_BOOTSTRAP_VERSIONS.items()})
        
        less, created = theme.themefile_set.get_or_create(name=filname)

        if created: msg = 'file created'
        else:       out = 'file saved'
            
        return self.render_to_response({
                'status': 'success', 'message': msg})


class DesignView(TemplateView):
    template_name = 'bootstrapit/design.html'

    def get_context_data(self, **kwargs):
        context = super(DesignView, self).get_context_data(**kwargs)
        context['theme_list'] = Theme.objects.filter(owner=self.request.user)
        return context

class DesignEditView(TemplateView):
    template_name = 'bootstrapit/design.html'

    def get_context_data(self, **kwargs):
        context = super(DesignEditView, self).get_context_data(**kwargs)
        context['theme'] = Theme.objects.get(slug=self.kwargs.get('theme'))
        return context


class HomeView(TemplateView):
    template_name = 'bootstrapit/home.html'

class Version(View):
    
    def get(self,context,**kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(BootstrapVersion,slug=slug)
        return HttpResponse(obj)


class JsonVersion(View):

    def get_context_data(self, **kwargs):
        context = super(JsonVersion, self).get_context_data(**kwargs)
        context['content_type']='application/json'
        return context
    
    def get(self,context,**kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(BootstrapVersion,slug=slug)
        return HttpResponse(
              obj.GetVar()  
            )
