from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.contrib import admin
from movies.models import *

admin.autodiscover()

urlpatterns = patterns('',
    ##### movie list and movie page #####
    url(r'^list/$',
        ListView.as_view(
            queryset=Movie.objects.all(),
            context_object_name='movie_list',
            template_name='movies/index.html')),
    url(r'^(?P<movie_id>\d+)/$', 'movies.views.detail'),
    url(r'^add/$', 'movies.views.add_movie'),
    url(r'^addlist/$', 'movies.views.add_movie_list'),
    url(r'^vote/$', 'movies.views.vote'),
    url(r'^review/$', 'movies.views.review'),
    url(r'^editreview/$', 'movies.views.edit_review'),
)
