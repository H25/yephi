from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from haystack.query import SearchQuerySet
from favoritelists.models import FavList
from movies.models import *
from newsfeed.models import *
from datetime import datetime
import random


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField('birthday', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile_picture',
                                        blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def get_relationships(self):
        relationships = Relationship.objects.filter(
            models.Q(from_user=self.user) |
            models.Q(to_user=self.user)
        )
        return relationships

    def has_relationship(self, visitor):
        flag = Relationship.objects.filter(from_user=self.user, to_user=visitor)
        if not flag:
            flag = Relationship.objects.filter(from_user=visitor, to_user=self.user)
        if flag:
            return True
        else:
            return False

    def get_requests(self):
        requests = RelationshipRequest.objects.filter(to_user=self.user)
        return requests

    def has_request(self, visitor):
        has_sent = RelationshipRequest.objects.filter(from_user=visitor, to_user=self.user)
        if has_sent:
            return 'sent request'
        else:
            has_received = RelationshipRequest.objects.filter(from_user=self.user, to_user=visitor)
            if has_received:
                return 'received request'
            else:
                return 'no request'

    def get_favlist(self):
        favlist = FavList.objects.filter(user=self.user)
        return favlist

    def has_in_favlist(self, movie):
        flag = FavList.objects.filter(user=self.user, movie=movie)
        if flag:
            return True
        else:
            return False

    def get_favgenre(self):
        favlist = self.get_favlist()
        favgenre = []
        for fav in favlist:
            genrelist = fav.movie.genre.split(', ')
            for genre in genrelist:
                if genre not in favgenre:
                    favgenre.append(genre)
        return favgenre

    def compare_favlist(self, visitor):
        favlist1 = FavList.objects.filter(user=self.user)
        favlist2 = FavList.objects.filter(user=visitor)
        avg_size = float(len(favlist1) + len(favlist2)) / 2
        if avg_size == 0:
            return 0
        similar = []
        for element1 in favlist1:
            for element2 in favlist2:
                if element1.movie == element2.movie:
                    similar.append(element1.movie)
        return round((len(similar) / avg_size) * 100)

    def has_reviewed(self, movie):
        ct = ContentType.objects.get(name='movie')
        flag = Comment.objects.filter(user=self.user, content_type=ct, object_pk=movie.id)
        if flag:
            return True
        else:
            return False

    def get_review(self, movie):
        ct = ContentType.objects.get(name='movie')
        review = Comment.objects.get(user=self.user, content_type=ct, object_pk=movie.id)
        return review.comment

    def get_add_list(self):
        mylist = Movie.objects.filter(added_by=self.user)
        return mylist

    def get_vote_list(self):
        mylist = Vote.objects.filter(user=self.user)
        return mylist

    def get_review_list(self):
        ct = ContentType.objects.get(name='movie')
        revlist = Comment.objects.filter(user=self.user, content_type=ct)
        mylist = []
        for rev in revlist:
            movie = Movie.objects.get(id=rev.object_pk)
            mylist.append(movie)
        return mylist

    def get_point(self):
        try:
            user_point = Points.objects.get(user=self.user)
        except:
            up = Points(user=self.user, point=0)
            up.save()
            user_point = Points.objects.get(user=self.user)
        return user_point.point

    def get_level(self):
        user_point = self.get_point()
        level = (Level.objects.filter(points_needed__lte=user_point)
                              .order_by('points_needed')
                              .reverse()[0])
        return level.name

    def get_recommend_movies(self):
        favgenre = self.get_favgenre()
        mylist = set()
        if not len(favgenre):
            #return 10 random movies
            mylist = Movie.objects.order_by('?')[:10]
        else:
            #return 10 (random) similar movies to the favorite genres of users
            results = SearchQuerySet().filter(genre__in=favgenre)
            while len(mylist) < 10:
                random_result = random.choice(results)
                movie = Movie.objects.get(id=int(random_result.pk))
                if not self.has_in_favlist(movie) and movie not in mylist:
                    mylist.add(movie)
        return mylist


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user')


class RelationshipType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationship_set_1')
    #define the related_name to avoid name conflict in Django after
    #creating database, User model (normally it will create attribute 'friend_set')
    to_user = models.ForeignKey(User, related_name='relationship_set_2')
    relationship_type = models.ForeignKey(RelationshipType)
    #there are many known bugs with auto_now_add=True
    #that's why don't use it eventhough it's more convenient
    created_at = models.DateTimeField('created at', default=datetime.now())

    def __unicode__(self):
        return '%s, %s, %s' % (self.from_user.username,
                               self.to_user.username,
                               self.relationship_type.name)


class RelationshipRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='relationship_request_set_1')
    to_user = models.ForeignKey(User, related_name='relationship_request_set_2')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', default=datetime.now())

    def __unicode__(self):
        return '%s, %s' % (self.from_user.username, self.to_user.username)
