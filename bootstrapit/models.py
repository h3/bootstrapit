# -*- coding: utf-8 -*-

from django.db import models
from bootstrapit.parser.parser import FileVarToJson
import os
from django.conf import settings
from django.core.urlresolvers import reverse


class BootstrapVersion(models.Model):
    version = models.CharField('version',max_length=255,unique=True)
    slug = models.SlugField('slug',max_length=255)
    url = models.URLField('depo url',max_length=255)
    store = models.CharField('store path',max_length=255,blank=True)

    def __unicode__(self):
        return "%s" % self.version

    def GetCssUrl(self):
        return os.path.join(settings.MEDIA_URL,self.store,'doc/assets/css/bootstrap.css')

    def GetCssUrl(self):
        return os.path.join(settings.MEDIA_URL,self.store,'doc/assets/js/bootstrap.min.js')

    def GetVar(self):
        return FileVarToJson(
                os.path.join(settings.MEDIA_ROOT,self.store,'less/variables.less')
                )
    
    def get_absolute_url(self):
        return reverse('bootstrapversion-home',args=(self.slug))

    

