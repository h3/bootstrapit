from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from bootstrapit.models import *


class DesignView(TemplateView):
    template_name = 'bootstrapit/design.html'
#   def get_context_data(self, **kwargs):
#       context = super(DesignView, self).get_context_data(**kwargs)
#       context['object_list'] = 
#       return context
