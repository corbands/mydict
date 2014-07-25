from django.conf.urls import url, patterns

from users import views
from users.views import EditProfileView, RegisterView, AuthView, AboutView, AccountView

urlpatterns = patterns('',
	url(r'^$', AccountView.as_view()),
	url(r'auth/$', AuthView.as_view(), name='auth'),

	url(r'register/$', RegisterView.as_view(), name='register'),

    url(r'about/$', views.AboutView.as_view(), name='about'),

	url(r'signout/$', views.signout, name='signout'),

	url(r'(?P<username>\w+)/settings/$', EditProfileView.as_view(), name='profile_edit'),

    url(r'(?P<username>\w+)/$', AccountView.as_view(), name='account'),
	)