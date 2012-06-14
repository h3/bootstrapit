# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView, View
from bootstrapit.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class HomeView(TemplateView):
    template_name = 'bootstrapit/home.html'

class Version(View):
    
    def get(self,context,**kwargs):
        slug = kwargs.get('slug')
        get_object_or_404(BootstrapVersion,slug=slug)
        return HttpResponse(
                'test'
            )
