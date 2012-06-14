# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView, BaseView
from bootstrapit.models import *


class HomeView(TemplateView):
    template_name = 'bootstrapit/home.html'

class Version(BaseView):
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return HTTPResponse(
                'test'
                )
