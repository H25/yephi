from django.http import HttpResponse
from movies.models import *
from favoritelists.models import *
from newsfeed.models import Feed
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.utils import simplejson


def add_to_favlist(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('user_id'):
            user = User.objects.get(id=int(GET['user_id']))
            movie = Movie.objects.get(id=int(GET['movie_id']))
            favlist = FavList(user=user, movie=movie)
            favlist.save()
            results = {'result': 'Added successfully'}

            #update feed
            f = Feed()
            f.update_feed(user, 7, None, movie)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
