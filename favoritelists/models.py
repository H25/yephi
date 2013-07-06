from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from datetime import datetime

class FavList(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    created_at = models.DateTimeField('created at', default=datetime.now())

    def __unicode__(self):
        return '%s %s' % (self.user, self.movie)