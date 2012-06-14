from bootstrapit.models import *
from django import forms


class BootstrapVersionForm(forms.ModelForm):

    class Meta:
        model = BootstrapVersion
        exclude = ('store',)

