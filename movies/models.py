from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=100, blank=True)
    actors = models.CharField(max_length=200, blank=True)
    plot = models.CharField(max_length=400, blank=True)
    poster = models.URLField(blank=True)
    runtime = models.CharField(max_length=20, blank=True)
    rating = models.CharField(max_length=10, blank=True)
    votes = models.CharField(max_length=20, blank=True)
    release_date = models.DateField('Released', blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    imdbid = models.CharField(max_length=10)
    added_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/movie/%i/" % self.id


class Vote(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    rate = models.IntegerField()

    def __unicode__(self):
        return '%s %s %f' % (self.user, self.movie, self.rate)
