# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bootstrapit.parser.parser import FileVarToJson


class BootstrapVersion(models.Model):
    version = models.CharField(_('version'),max_length=255,unique=True)
    slug = models.SlugField(_('slug'),max_length=255)
    url = models.URLField(_('depo url'),max_length=255)
    store = models.CharField(_('store path'),max_length=255,blank=True)

    def __unicode__(self):
        return "%s" % self.version

    def GetCssUrl(self):
        return os.path.join(settings.MEDIA_URL,self.store,'doc/assets/css/bootstrap.css')

    def GetJsUrl(self):
        return os.path.join(settings.MEDIA_URL,self.store,'doc/assets/js/bootstrap.min.js')

    def GetVar(self):
        return FileVarToJson(
                os.path.join(settings.MEDIA_ROOT,self.store,'less/variables.less')
                )
    class Meta:
        ordering = ('version',)
    
    def get_absolute_url(self):
        return "/"
        #return reverse('bootstrapversion-home',args=(self.slug))


class LessBaseFile(models.Model):
    content = models.TextField(_('Content'))
    name = models.CharField(_('Name'),max_length=255)
    slug = models.SlugField(_('slug'),max_length=255)
    BVersion = models.ForeignKey(BootstrapVersion)

    class Meta:
        unique_together = ("name","BVersion")
        ordering = ('BVersion','name')

    def get_absolute_url(self):
        return ''

    def __unicode__(self):
        return "%s (%s)" % (self.name,self.BVersion)

class Theme(models.Model):
    created = models.DateTimeField(_('created'))
    owner = models.ForeignKey(User)


class LessVertionFile(models.Model):
    file = models.ForeignKey(LessBaseFile)
    parent = models.ForeignKey("self",null=True,blank = True)
    project = models.ForeignKey(Theme)
    last_access = models.DateTimeField(_('last access'),auto_now = True,editable=False)

    

