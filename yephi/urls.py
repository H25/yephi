from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'yephi.views.home'),
    (r'^recommendation$', 'yephi.views.recommendation'),
    (r'^s/', 'yephi.views.search_autocomplete'),

    (r'^admin/', include(admin.site.urls)),
    (r'^user/', include('accounts.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^movie/', include('movies.urls')),
    (r'^favorite/', include('favoritelists.urls')),
    (r'^search/', include('haystack.urls')),
)

urlpatterns += staticfiles_urlpatterns()

# for development only
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
