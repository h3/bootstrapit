# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
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


class EditorBackend(ProcessFormView, JSONResponseMixin):
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        filename = request.POST.get('filename')
        if not (content and filename):
            return self.render_to_response({'status': 'fail',
                                            'message' :'content or filname not found'})
        #get bootstrap version
        v  = request.session.get('version')
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
                    'message' :'Bootstrap Theme not found',
                    'choices' : [{'pk' :u.pk,'created': u.created} for u in Theme.objects.filter(owner=request.user)]})

        try:
            th = Theme.objects.get(pk=th, owner = request.user)
        except:
            return self.render_to_response({'status': 'theme-404',
                    'message' :'Bootstrap Theme not found',
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
