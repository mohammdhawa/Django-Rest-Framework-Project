from django.urls import path
# from .views import movie_list_api, movie_detail_api
from .views import MovieListAPI, MovieDetailAPI


urlpatterns = [
    path('list', MovieListAPI.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailAPI.as_view(), name='movie-detail'),
    # path('list', movie_list_api, name='movie-list'),
    # path('<int:pk>', movie_detail_api, name='movie-detail'),
]