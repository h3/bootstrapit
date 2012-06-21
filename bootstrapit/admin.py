# -*- coding: utf-8 -*-

import reversion

from django.conf import settings
from django.contrib import admin
#from django.utils.translation import ugettext_lazy as _
#from webcore.utils.admin import AdminThumbnailMixin
#from grappellifit.admin import TranslationAdmin
from bootstrapit.models import *
from bootstrapit.forms import *


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name','slug','owner','bootstrap_version')
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Theme, ThemeAdmin)


class ThemeFileAdmin(reversion.VersionAdmin):
    list_display = ('name', 'theme', 'date_modified',)
admin.site.register(ThemeFile, ThemeFileAdmin)


# TODO: remove (deprecated)
class BootstrapVersionAdmin(admin.ModelAdmin):
    list_display = ('version','slug','url','store','get_absolute_url')
    prepopulated_fields = {"slug": ("version",)}
    form = BootstrapVersionForm
admin.site.register(BootstrapVersion,BootstrapVersionAdmin)
