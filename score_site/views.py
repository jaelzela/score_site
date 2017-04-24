# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect

###########################
####     Controllers   ####
###########################
def index(request):
    return HttpResponseRedirect('/score_site/score')