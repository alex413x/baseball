from django.conf.urls import url, include

from . import views

urlpatterns= [
    url(r'^matches/$', views.MatchList.as_view()),
    url(r'^match/(?P<pk>[0-9]+)/$', views.MatchDetail.as_view()),
    url(r'^players/$', views.PlayerList.as_view()),
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetail.as_view()),
    url(r'^pitches/$', views.PitchList.as_view()),
    url(r'^pitch/(?P<pk>[0-9]+)/$', views.PitchDetail.as_view()),
    url(r'^stats/$', views.StatList.as_view()),
    url(r'^stat/(?P<pk>[0-9]+)/$', views.StatDetail.as_view()),
    url(r'^throw_pitch/$', views.throw_pitch, name='thow_pitch'),
    url(r'^load_player/(?P<playerID>[\w.@+-]+)/$', views.load_player, name='load_player'),
    url(r'^load_averages/$', views.load_averages, name='load_averages'),

    url(r'^django-rq/', include('django_rq.urls')),

	url(r'^$', views.index, name='index'),
	#url(r'^lchat/(?P<pk>[0-9]+)$', views.lBotDetail.as_view())
    #url(r'^lchat/bots$', views.lBotList.as_view()),
]