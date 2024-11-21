from django.urls import path
from .views import movie_list_api, movie_detail_api


urlpatterns = [
    path('list', movie_list_api, name='movie-list'),
    path('<int:pk>', movie_detail_api, name='movie-detail'),
]