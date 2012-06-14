# -*- coding: utf-8 -*-

from django.db import models
from bootstrapit.parser.parser import FileVarToJson
import os


class BootstrapVersion(models.Model):
    version = models.CharField('version',max_length=255,unique=True)
    slug = models.SlugField('slug',max_length=255)
    url = models.URLField('depo url',max_length=255)
    store = models.CharField('store path',max_length=255,blank=True)

    def __unicode__(self):
        return "%s" % self.version

    def GetCss(self):
        return ''

    def GetVar(self):
        return FileVarToJson(
                os.path.join(self.store,'less/variables.less')
                )

    

