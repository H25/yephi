from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from accounts.models import *
from newsfeed.models import *
from movies.models import *
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
from django.utils import simplejson
from django.views.decorators.http import require_GET


@login_required(login_url='/user/login/')
def home(request):
    sent_request = FeedAction.objects.get(id=1)
    feeds = Feed.objects.all().order_by('-created_at').exclude(action=sent_request)
    new_movies = Movie.objects.all().order_by('-release_date')[:10]

    return render_to_response('index.html', {
        'feeds': feeds,
        'new_movies': new_movies,
    }, context_instance=RequestContext(request))


@login_required(login_url='/user/login/')
def recommendation(request):
    recommended_movies = request.user.get_profile().get_recommend_movies()

    return render_to_response('recommendation.html', {
        'recommended_movies': recommended_movies
    }, context_instance=RequestContext(request))


@require_GET
def search_autocomplete(request):
    query = request.GET['q']

    results = SearchQuerySet().autocomplete(content_auto=query)

    resp = [r.object.title for r in results]
    json = simplejson.dumps(resp)
    return HttpResponse(json, mimetype='application/json')
