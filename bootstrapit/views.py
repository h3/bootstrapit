# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import ProcessFormView
from datetime import datetime

from bootstrapit.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json  
from django import http  


class EditorView(TemplateView):
    template_name = 'bootstrapit/editor.html'

#   def post(self, request, *args, **kwargs):
#       return http.HttpResponse(content,  
#                                content_type='application/json',  
#                                **httpresponse_kwargs)  

class JSONResponseMixin(object):  
    def render_to_response(self, context):  
        "Returns a JSON response containing 'context' as payload"  
        return self.get_json_response(self.convert_context_to_json(context))  
  
    def get_json_response(self, content, **httpresponse_kwargs):  
        "Construct an `HttpResponse` object."  
        return http.HttpResponse(content,  
                                 content_type='application/json',  
                                 **httpresponse_kwargs)  
  
    def convert_context_to_json(self, context):  
        "Convert the context dictionary into a JSON object"  
        # Note: This is *EXTREMELY* naive; in reality, you'll need  
        # to do much more complex handling to ensure that arbitrary  
        # objects -- such as Django model instances or querysets  
        # -- can be serialized as JSON.  
        return json.dumps(context)


class EditorBackend(JSONResponseMixin, View): #, ProcessFormView
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
