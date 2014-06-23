from django.conf.urls import url, patterns

from users import views



urlpatterns = patterns('',
	url(r'^$', views.auth, name='auth'),
	url(r'auth/$', views.auth, name='auth'),

	url(r'register/$', views.register, name='register'),

    url(r'about/$', views.about, name='about'),

	url(r'auth_check/$', views.auth_check, name='auth_check'),
	url(r'register_check/$', views.register_check, name='register_check'),
	url(r'signout/$', views.signout, name='signout'),

	url(r'user/settings/$', views.edit_profile, name='edit_profile'),
	url(r'user/settings/edited$', views.profile_edited, name='profile_edited'),

    url(r'user/(?P<username>\w+)$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/(?P<page_number>\d+)$', views.account, name='account'),
	)