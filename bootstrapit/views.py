# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView, View
from datetime import datetime

from bootstrapit.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

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
        get_object_or_404(BootstrapVersion,slug=slug)
        return HttpResponse(
                'test'
            )
