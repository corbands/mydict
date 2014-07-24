from django.conf.urls import url, patterns

from words import views

urlpatterns = patterns('',	
	url(r'(?P<word_id>\d+)/edited$', views.word_edited, name='word_edited'),
	url(r'(?P<word_id>\d+)$', views.word_edit, name='word_edit'),
	url(r'$', views.word_edit, name='word_edit_template'),
)