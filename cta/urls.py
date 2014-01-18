from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    # ex: /
    url(r'^$', views.index, name='index'),
)