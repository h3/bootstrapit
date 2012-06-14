from bootstrapit.models import *
from django import forms
from git import *
import random

class BootstrapVersionForm(forms.ModelForm):

    class Meta:
        model = BootstrapVersion
        exclude = ('store',)
    store = ""


    def clean_url(self):
        url = self.cleaned_data['url']
        tmp = ''.join([random.choice('0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN_') for u in range(0,25)])
        #try:
        print url
        repo = Repo.init(url)
        repo.clone('/tmp/%s'% tmp)

        #except:
        raise forms.ValidationError('Url non valide pour Git')
        return url


    def save(self,commit=False):
        v = super(BootstrapVersionForm,self).save(commit)
        v.url = self.cleaned_data['url']
        v.store = "test"

        return v



