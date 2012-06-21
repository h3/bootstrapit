# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bootstrapit.parser.parser import FileVarToJson

from bootstrapit.conf import settings

VERSIONS = settings.BOOTSTRAPIT_BOOTSTRAP_VERSIONS.items()


class Theme(models.Model):
    """
    This model holds saved custom themes
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    owner = models.ForeignKey(User, related_name="owner")
    contributors = models.ManyToManyField(User, related_name="contributors", blank=True, null=True)
    bootstrap_version = models.CharField(_('version'), 
                            max_length=20, choices=VERSIONS)

    date_created  = models.DateTimeField(_('created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('created'), auto_now=True)
    rendered_css = models.TextField(_('rendered CSS'), blank=True, null=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.bootstrap_version)


class ThemeFile(models.Model):
    theme = models.ForeignKey(Theme)
    name = models.CharField(_('filename'), max_length=255)
    content = models.TextField(_('content'))
    date_modified = models.DateTimeField(_('created'), auto_now=True)

    def __unicode__(self):
        return u'%s' % self.name


    
# TODO: remove (deprecated)
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


class LessVertionFile(models.Model):
    file = models.ForeignKey(LessBaseFile)
    parent = models.ForeignKey("self",null=True,blank = True)
    project = models.ForeignKey(Theme)
    last_access = models.DateTimeField(_('last access'),auto_now = True,editable=False)
