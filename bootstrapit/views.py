# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, DetailView
from bootstrapit.models import *


class HomeView(TemplateView):
    template_name = 'bootstrapit/home.html'
