from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from accounts.models import *
from newsfeed.models import *
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.auth.decorators import login_required


@login_required(login_url='/user/login/')
def detail(request, user_id):
    owner = get_object_or_404(User, pk=user_id)
    try:
        owner_profile = owner.get_profile()
    except:  # raise exception
        # create new profile
        up = UserProfile(user=owner)
        up.save()
        owner_profile = owner.get_profile()

    owner_relationships = owner_profile.get_relationships()
    owner_requests = owner_profile.get_requests()
    owner_favlist = owner_profile.get_favlist()
    owner_favgenre = owner_profile.get_favgenre()
    owner_added = owner_profile.get_add_list()
    owner_voted = owner_profile.get_vote_list()
    owner_reviewed = owner_profile.get_review_list()
    owner_point = owner_profile.get_point()
    owner_level = owner_profile.get_level()

    return render_to_response('accounts/userprofile.html', {
        'owner': owner,
        'owner_profile': owner_profile,
        'owner_relationships': owner_relationships,
        'owner_requests': owner_requests,
        'owner_favlist': owner_favlist,
        'owner_favgenre': owner_favgenre,
        'owner_added': owner_added,
        'owner_voted': owner_voted,
        'owner_reviewed': owner_reviewed,
        'owner_point': owner_point,
        'owner_level': owner_level
    }, context_instance=RequestContext(request))


def userprofile(request):
    userprofile_url = '/user/%d/' % request.user.id
    return HttpResponseRedirect(userprofile_url)


@login_required(login_url='/user/login/')
def edit_profile(request):
    try:
        profile = request.user.get_profile()
    except:
        up = UserProfile(user=request.user)
        up.save()
        profile = request.user.get_profile()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/profile/')
    else:
        form = UserProfileForm(instance=profile)

    return render_to_response('accounts/edit_profile.html', {
        'form': form,
        'profile': profile
    }, context_instance=RequestContext(request))


@login_required(login_url='/user/login/')
def relationship_request(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        GET = request.GET
        if 'request_type' in GET:
            if GET['request_type'] == 'send':
                #save request to database
                f_user = User.objects.get(id=int(GET['from_user_id']))
                t_user = User.objects.get(id=int(GET['to_user_id']))
                gmessage = GET['message']
                request = RelationshipRequest(from_user=f_user,
                                              to_user=t_user,
                                              message=gmessage)
                request.save()

                #prepare json response
                results = {'result': 'Sent successfully'}

                #update feed
                f = Feed()
                f.update_feed(f_user, 1, t_user, None)

            elif GET['request_type'] == 'accept':
                #save relationship
                f_user = User.objects.get(id=int(GET['from_user_id']))
                t_user = User.objects.get(id=int(GET['to_user_id']))
                rel_type = RelationshipType.objects.get(name='Friend')
                relationship = Relationship(from_user=f_user,
                                            to_user=t_user,
                                            relationship_type=rel_type)
                relationship.save()
                request = RelationshipRequest.objects.get(from_user=f_user,
                                                          to_user=t_user)
                request.delete()

                #prepare json response
                results = {'result': 'Accept successfully'}

                #update feed
                f = Feed()
                f.update_feed(t_user, 2, f_user, None)

    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required(login_url='/user/login/')
def comment_feed(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        GET = request.GET
        if 'f_user' in GET:
            #save request to database
            f_user = User.objects.get(id=int(GET['f_user']))
            t_user = User.objects.get(id=int(GET['t_user']))

            #update feed
            f = Feed()
            f.update_feed(f_user, 4, t_user, None)

            results = {'result': 'Successful'}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
