from django.conf.urls import url

from fp import views

urlpatterns = [
    url(r'first', views.first, name='first'),
    url(r'second', views.second, name='second'),
    url(r'third', views.third, name='third'),
    url(r'first_fn', views.first_fn, name='first_fn'),
    url(r'second_fn', views.second_fn, name='second_fn'),
    url(r'third_fn', views.third_fn, name='third_fn'),
]