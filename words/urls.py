from django.conf.urls import url, patterns

from words import views

urlpatterns = patterns('',	
	url(r'word/(?P<word_id>\d+)/$', views.word_edit, name='word_edit'),
	url(r'word/(?P<word_id>\d+)/edited$', views.word_edited, name='word_edited'),
)