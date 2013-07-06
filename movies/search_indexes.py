from haystack.indexes import *
from haystack import site
from movies.models import Movie


class MovieIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    plot = CharField(model_attr='plot')
    genre = CharField(model_attr='genre')
    rating = CharField(model_attr='rating')

    content_auto = EdgeNgramField(model_attr='title')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Movie.objects.all()


site.register(Movie, MovieIndex)
