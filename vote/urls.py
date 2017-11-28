from django.conf.urls import url
from . import views

urlpatterns = [
    #/
    url(r'^$', views.landing, name='landing'),
    #home/ --homepage
    url(r'^home/$', views.home, name='home'),
    #mypolls/ -- show polls
    url(r'^mypolls/$', views.PollList.as_view(), name='poll-list'),
    #poll/details/<pk>
    url(r'^poll/details/(?P<pk>[0-9]+)/$', views.PollDetails.as_view(), name='poll-details'),
    #create/
    url(r'^create/$', views.create, name='create'),
    #vote/<question_id>/
    url(r'^vote/(?P<question_id>[0-9]+)/$', views.vote, name='vote1'),
    #poll/results/<pk>
    url(r'poll/results/(?P<pk>[0-9]+)/$', views.PollResults.as_view(), name='results')
]