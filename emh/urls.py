from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + patterns('',
    # Examples:
    # url(r'^$', 'emh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'word/', include('words.urls', namespace='words')),
    url(r'', include('users.urls', namespace='users')),
)
