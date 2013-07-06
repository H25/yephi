from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from datetime import datetime


class FeedAction(models.Model):
    name = models.CharField(max_length=200)
    point = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class Feed(models.Model):
    from_user = models.ForeignKey(User, related_name='newsfeed_set_1')
    action = models.ForeignKey(FeedAction)
    to_user = models.ForeignKey(User, related_name='newsfeed_set_2', null=True)
    to_movie = models.ForeignKey(Movie, null=True)
    is_read = models.BooleanField(blank=True)
    created_at = models.DateTimeField('created at', default=datetime.now())

    def __unicode__(self):
        return '%s %s %s %s at %s' % (self.from_user,
                                      self.action,
                                      self.to_user,
                                      self.to_movie,
                                      self.created_at)

    def get_latest_feed(self, limit=100):
        #get a limit (default 100) latest feeds
        feeds = Feed.objects.order_by('created_at')[:limit]
        return feeds

    def update_feed(self, from_user, action_id, to_user=None, to_movie=None):
        action = FeedAction.objects.get(id=action_id)
        self = Feed(from_user=from_user,
                    action=action,
                    to_user=to_user,
                    to_movie=to_movie,
                    is_read=False,
                    created_at=datetime.now())
        self.save()
        try:
            user_points = Points.objects.get(user=from_user)
            user_points.point += action.point
            user_points.save()
        except:
            user_points = Points(user=from_user, point=action.point)
            user_points.save()


class Points(models.Model):
    user = models.ForeignKey(User)
    point = models.IntegerField()


class Level(models.Model):
    points_needed = models.IntegerField()
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % (self.name)
