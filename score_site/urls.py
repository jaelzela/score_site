from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from score_site import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score/', include('score.urls', namespace="score")),
    url(r'^rate/', include('rate.urls', namespace="rate")),
    url(r'^info/', include('info.urls', namespace="info")),
    url(r'^fp/', include('fp.urls', namespace="fp")),
    #url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns()