from django.shortcuts import render
from django.http import Http404
from .models import Actor, Movie
from django.views.generic import DetailView


def index(request):
    actors = None
    movies = None
    if q := request.GET.get('search'):
        actors = Actor.objects.filter(name__icontains=q)
        movies = Movie.objects.filter(name__icontains=q)
    return render(request, 'csfd_search/index.html', {'actors': actors,
                                                      'movies': movies,
                                                      'query': q})


class ActorDetail(DetailView):
    model = Actor
    template_name = 'csfd_search/detail.html'

    def get(self, request, *args, **kwargs):
        actor_id = kwargs['pk']
        try:
            actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            raise Http404("Actor does not exists.")
        movies = Movie.objects.filter(actors=actor_id).order_by('name')
        return render(request, self.template_name, {'actor': actor,
                                                    'movies': movies})


class MovieDetail(DetailView):
    model = Movie
    template_name = 'csfd_search/detail.html'

    def get(self, request, *args, **kwargs):
        movie_id = kwargs['pk']
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise Http404("Movie does not exists.")
        movies = Actor.objects.filter(movie=kwargs['pk']).order_by('name')
        return render(request, self.template_name, {'movie': movie,
                                                    'actors': movies})
