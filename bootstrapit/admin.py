# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
#from django.utils.translation import ugettext_lazy as _
#from webcore.utils.admin import AdminThumbnailMixin
#from grappellifit.admin import TranslationAdmin
from bootstrapit.models import *
from bootstrapit.forms import *


class BootstrapVersionAdmin(admin.ModelAdmin):
    list_display = ('version','slug','url','store','get_absolute_url')
    prepopulated_fields = {"slug": ("version",)}
    form = BootstrapVersionForm
admin.site.register(BootstrapVersion,BootstrapVersionAdmin)
