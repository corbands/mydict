from django.conf.urls import url, patterns

from users import views
from users.views import EmhUserView, RegisterView, AuthView, AboutView

urlpatterns = patterns('',
	url(r'^$', AuthView.as_view(), name='auth'),
	url(r'auth/$', AuthView.as_view(), name='auth'),

	url(r'register/$', RegisterView.as_view(), name='register'),

    url(r'about/$', views.AboutView.as_view(), name='about'),

	url(r'signout/$', views.signout, name='signout'),

	url(r'user/(?P<username>\w+)/settings/$', EmhUserView.as_view(), name='profile_edit'),
	# url(r'user/settings/$', EmhUserView.as_view(), name='profile_edit'),

    url(r'user/(?P<username>\w+)$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/$', views.account, name='account'),
    url(r'user/(?P<username>\w+)/(?P<page_number>\d+)$', views.account, name='account'),
	)