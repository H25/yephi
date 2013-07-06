from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import *
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.conf import settings

from movies.forms import *
from movies.models import *
from newsfeed.models import Feed
from favoritelists.models import *

from datetime import datetime
import time
import urllib2


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    total = Vote.objects.filter(movie=movie).count()
    avg = Vote.objects.filter(movie=movie).aggregate(Avg('rate'))
    user_voted = Vote.objects.filter(movie=movie, user=request.user.id)
    favusers = FavList.objects.filter(movie=movie)
    return render_to_response('movies/moviepage.html', {
        'movie': movie,
        'avg_rate': avg['rate__avg'],
        'total_votes': total,
        'favusers': favusers,
        'user_voted': user_voted
    }, context_instance=RequestContext(request))


def _save_movie(imdb_id, user):
    request_url = 'http://www.omdbapi.com/?i=%s' % imdb_id
    errors = []

    try:
        response = urllib2.urlopen(request_url)
    except urllib2.URLError as err:
        errors.append(err)
    if response:
        result = response.read()
        json_result = simplejson.loads(result)

        if json_result['Response'] != 'False':
            # process data
            title = json_result['Title']
            year = json_result['Year']

            # process release date
            release_str = json_result['Released']
            if len(release_str.split()) == 1:
                if release_str == 'N/A':
                    release_time = None
                else:
                    release_time = datetime(*time.strptime(release_str, "%Y")[:6])
            elif len(release_str.split()) == 2:
                release_time = datetime(*time.strptime(release_str, "%b %Y")[:6])
            elif len(release_str.split()) == 3:
                release_time = datetime(*time.strptime(release_str, "%d %b %Y")[:6])

            # fetch poster image to local disk
            poster_url = json_result['Poster']
            poster_file_name = ('/images/posters/%s_%s.jpg' %
                                (year, title.lower().replace(' ', '_')))
            poster_file_abs = settings.MEDIA_ROOT + poster_file_name
            poster_file_rel = '/media' + poster_file_name
            if poster_url == 'N/A':
                poster_file_rel = '/media/images/default_poster.png'
            else:
                try:
                    resp = urllib2.urlopen(poster_url)
                except urllib2.URLError as err:
                    print err
                if resp:
                    poster_file = open(poster_file_abs, 'w')
                    poster_file.write(resp.read())
                    poster_file.close()

            # check if movie exists in DB
            flag = Movie.objects.filter(title=title, year=year)
            if not flag:  # add movie info to DB
                new_movie = Movie(
                    title=title,
                    year=year,
                    genre=json_result['Genre'],
                    actors=json_result['Actors'],
                    plot=json_result['Plot'],
                    poster=poster_file_rel,
                    runtime=json_result['Runtime'],
                    rating=json_result['imdbRating'],
                    votes=json_result['imdbVotes'],
                    release_date=release_time,
                    added_by=user,
                    imdbid=imdb_id
                )
                new_movie.save()

                # update feed
                f = Feed()
                f.update_feed(user, 3, None, new_movie)
        else:
            errors.append('No data available')
    else:  # duplicate movie, returns error
        errors.append('This movie is already in our database. '
                      'Please try to add another one.')
    # return errors list
    return errors


@login_required(login_url='/user/login/')
def add_movie(request):
    response = ''
    if request.method == 'POST':
        imdb_url = request.POST['link']
        # format: http://www.imdb.com/title/tt1298650/
        if imdb_url.find('http://www.imdb.com/title/') == 0:
            imdb_id = imdb_url.split('/')[4]
            errors = _save_movie(imdb_id, request.user)
            if errors == []:
                response = 'Added successfully'
            else:
                response = errors
        else:
            response = 'Invalid URL'

    return render_to_response('movies/add_movie.html', {
        'response': response,
    }, context_instance=RequestContext(request))


@login_required(login_url='/user/login/')
def add_movie_list(request):
    success_times = 0
    fail_times = 0
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            destination = open(settings.MEDIA_ROOT + '/movielist.txt', 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
            # open file and extract data
            with open(settings.MEDIA_ROOT + '/movielist.txt') as f:
                for line in f.readlines():
                    if line.find('http://www.imdb.com/title/') == 0:
                        imdb_id = line.split('/')[4]
                        errors = _save_movie(imdb_id, request.user)
                        if errors == []:
                            success_times += 1
                        else:
                            fail_times += 1
                    else:
                        fail_times += 1
    else:
        form = UploadFileForm()
    return render_to_response('movies/add_movies.html', {
        'form': form,
        'success': success_times,
        'fail': fail_times,
    }, context_instance=RequestContext(request))


@login_required(login_url='/user/login/')
def vote(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        GET = request.GET
        if 'rate' in GET:
            #save request to database
            user = User.objects.get(id=int(GET['user_id']))
            movie = Movie.objects.get(id=int(GET['movie_id']))
            try:
                vote = Vote.objects.get(user=user, movie=movie)
                vote.rate = int(GET['rate'])
                vote.save()
            except:
                rate = int(GET['rate'])
                new_vote = Vote(user=user, movie=movie, rate=rate)
                new_vote.save()

            total = Vote.objects.filter(movie=movie).count()
            avg = Vote.objects.filter(movie=movie).aggregate(Avg('rate'))
            #prepare json response
            results = {'result': 'Successful', 'total': total, 'avg': avg['rate__avg']}

            #update feed
            f = Feed()
            f.update_feed(user, 6, None, movie)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required(login_url='/user/login/')
def review(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        GET = request.GET
        if 'user_id' in GET:
            #save request to database
            user = User.objects.get(id=int(GET['user_id']))
            movie = Movie.objects.get(id=int(GET['movie_id']))

            #update feed
            f = Feed()
            f.update_feed(user, 5, None, movie)

            results = {'result': 'Successful'}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required(login_url='/user/login/')
@require_POST
def edit_review(request):
    data = request.POST.copy()
    #get data from POST request
    username = data.get('name')
    user = User.objects.get(username=username)
    content_type = ContentType.objects.get(name='movie')
    object_pk = data.get('object_pk')
    next = data.get('next')

    #edit the review
    review = Comment.objects.get(user=user, content_type=content_type, object_pk=object_pk)
    review.comment = data.get('comment')
    review.save()

    #redirect to 'next' destination
    return HttpResponseRedirect(next)
