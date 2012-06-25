# -*- coding: utf-8 -*-

from datetime import datetime
import reversion

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
        theme_id = request.POST.get('theme_id')
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
        
        less, created = theme.themefile_set.get_or_create(name=filename)
        msg = created and 'file created' or 'file saved'


        # We don't want to make an unecessary hit to the db
        # if the object already exists.
        if not created and less.content == content:
            return self.render_to_response({
                    'status': 'success', 'message': "Nothing changed"})
        else:
            with reversion.create_revision():
                less.content = content
                less.save()
                reversion.set_user(self.request.user)
                # TODO: find something more useful as msg
                reversion.set_comment("Changed content")

            return self.render_to_response({
                    'status': 'success', 'message': msg})

from django.views import static
class FileBackend(ProcessFormView, JSONResponseMixin):
    """
    Handles files
    """
    def get(self, request, *args, **kwargs):
        theme = get_object_or_404(Theme, slug=kwargs.get('theme'))

        try:
            # return file from db
            document = theme.themefile_set.get(name=kwargs.get('filepath'))
            return HttpResponse(document.content)
        except ThemeFile.DoesNotExist:
            # return real static file
            url = theme.get_static_url() + kwargs.get('filepath')
            return static.serve(request, url, document_root=settings.MEDIA_ROOT)


        return self.render_to_response({
                'status': 'success', 'message': '%s' % kwargs.get('filepath')})

    def post(self, request, *args, **kwargs):
        theme_id = request.POST.get('theme_id')
        filename = request.POST.get('filename')
        content  = request.POST.get('content')

        return self.render_to_response({
                'status': 'success', 'message': msg})
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
        
        less, created = theme.themefile_set.get_or_create(name=filename)
        msg = created and 'file created' or 'file saved'

        less.content = content

        with reversion.create_revision():
            less.save()
            reversion.set_user(self.request.user)
            reversion.set_comment("Changed content")

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
