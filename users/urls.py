from django.conf.urls import url, patterns

from users import views
from users.views import EmhUserView

urlpatterns = patterns('',
	url(r'^$', views.auth, name='auth'),
	url(r'auth/$', views.auth, name='auth'),

	url(r'register/$', views.register, name='register'),

    url(r'about/$', views.about, name='about'),

	url(r'auth_check/$', views.auth_check, name='auth_check'),
	url(r'register_check/$', views.register_check, name='register_check'),
	url(r'signout/$', views.signout, name='signout'),

	url(r'user/settings/$', EmhUserView.as_view(), name='profile_edit'),

    url(r'user/(?P<username>\w+)$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/(?P<page_number>\d+)$', views.account, name='account'),
	)