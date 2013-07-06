from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.contrib import admin
from favoritelists.models import *

admin.autodiscover()

urlpatterns = patterns('',
    
    ##### user list and profile page #####

    url(r'^$',
        ListView.as_view(
            queryset = FavList.objects.all(),
            context_object_name = 'fav_list',
            template_name = 'favourite/index.html')),
    #url(r'^(?P<fav_id>\d+)/$', 'favoritelists.views.detail'),

    url(r'^add/$', 'favoritelists.views.add_to_favlist'),
)