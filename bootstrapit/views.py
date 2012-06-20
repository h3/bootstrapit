# -*- coding: utf-8 -*-

import json  
from datetime import datetime

from django import http  
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import ProcessFormView

from bootstrapit.models import *
from bootstrapit.conf import settings
from bootstrapit.utils import JSONResponseMixin


class EditorView(TemplateView):
    template_name = 'bootstrapit/editor.html'

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        context['bootstrap_nav'] = settings.BOOTSTRAPIT_BOOTSTRAP_NAV['2.1']
        return context


class EditorBackend(ProcessFormView, JSONResponseMixin):
    def post(self, request, *args, **kwargs):
        return self.render_to_response({'test': 'test1'})


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
