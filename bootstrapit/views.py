# -*- coding: utf-8 -*-

import json  
from datetime import datetime

from django import http  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import ProcessFormView

from bootstrapit.models import *
from bootstrapit.conf import settings
from bootstrapit.utils import JSONResponseMixin




class EditorView(TemplateView):
    template_name = 'bootstrapit/editor.html'

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        context['bootstrap_nav'] = settings.BOOTSTRAPIT_BOOTSTRAP_NAV['2.0.4']
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
        #get bootstrap version
        v  = request.session.get('version')

        try:
            theme = Theme.objects.get(pk=theme_id, owner=request.user) # TODO: OR CONTRIBUOR
        except Theme.DoesNotExist:
            return self.render_to_response({'status':  'error',
                                            'message': 'Theme not found'})


        if not v:
            return self.render_to_response({'status': 'BV',
                    'message' :'Bootstrap Version not found',
                    'choices' : [{'pk': u.pk,'name' : u.version} for u in BootstrapVersion.objects.all()]})

        try:
            v = BootstrapVersion.objects.get(slug=v)
        except:
            return self.render_to_response({'status': 'BV-404',
                    'message' :'Bootstrap Version not found',
                    'choices' : [{'pk': u.pk,'name' : u.version} for u in BootstrapVersion.objects.all()]})
        
        #get theme
        th = request.session.get('theme')
        if not th:
            return self.render_to_response({'status': 'theme',
                    'message' :'Theme not found',
                    'choices' : [{'pk' :u.pk,'name': u.created} for u in Theme.objects.filter(owner=request.user)]})

        try:
            th = Theme.objects.get(pk=th, owner = request.user)
        except:
            return self.render_to_response({'status': 'theme-404',
                    'message' :'Theme not found',
                    'choices' : [{'pk' :u.pk,'created': u.created} for u in Theme.objects.filter(owner=request.user)]})

        #get LessBaseFile associate
        lessBase = LessBaseFile.objects.filter(name = filname,BVersion = v)[:1]
        if not lessBase:
            return self.render_to_response({'status': 'file',
                    'message' :'No less file find with this name',
                    'choices' : [{'pk' : u.pk, 'name' : u.name } for u in LessBaseFile.objects.filter(BVersion=v)]})

        #get last upload of this file vertion
        last = LessVertionFile.objects.filter(project = th, file = lessBase).order_by('+last_access')[:1]

        if last:
            last = last[0]
        else:
            last = None
        
        #creat an save LessVertionFile
        LessVertionFile.objects.create(file = lessBase,
                                       parent = last,
                                       project = th)

        return self.render_to_response({'status': 'ok',
                                        'message' : 'file save'})


class DesignView(TemplateView):
    template_name = 'bootstrapit/design.html'
#   def get_context_data(self, **kwargs):
#       context = super(DesignView, self).get_context_data(**kwargs)
#       context['object_list'] = 
#       return context


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
