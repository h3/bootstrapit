# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand#, CommandError
from bootstrapit.models import BootstrapVersion
#from django.db.models import Q

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for u in BootstrapVersion.objects.all():
            print ('récupérations des fichiers pour %s récupérés' % u)
            u.save()
            print ('fichiers pour %s récupérés' % u)
        print ("tous les fichiers on été récupérés")
