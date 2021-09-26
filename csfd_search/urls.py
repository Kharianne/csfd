from django.urls import path

from .views import index, ActorDetail, MovieDetail

urlpatterns = [
    path('', index, name='home'),
    path('actor/<int:pk>/', ActorDetail.as_view(), name='actor_detail'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='movie_detail')
]