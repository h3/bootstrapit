# -*- coding: utf-8 -*-

from bootstrapit.models import *
from django import forms
import git
import random
from django.conf import settings

class BootstrapVersionForm(forms.ModelForm):

    class Meta:
        model = BootstrapVersion
        exclude = ('store',)
    store = ""


    def clean_url(self):
        url = self.cleaned_data['url']
        ver = self.cleaned_data['version']
        #tmp = ''.join([random.choice('0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN_') for u in range(0,25)])
        try:
            dest = '%s/bootstrap/%s' % (settings.MEDIA_ROOT,ver)
            os.system('rm -rf %s' % dest)
            os.system('mkdir -p %s' % dest)
            git.Git().clone(url,dest)
            os.system('cd %s && make > /dev/null' % dest)
            self.store = "bootstrap/%s" % ver
        except:
            raise forms.ValidationError('Url non valide pour Git, ou il y a eu une erreur à l\'estraction')
        return url


    def save(self,commit=False):
        v = super(BootstrapVersionForm,self).save(commit)
        v.url = self.cleaned_data['url']
        v.store = self.store

        return v



