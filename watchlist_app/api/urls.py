from django.urls import path
# from .views import movie_list_api, movie_detail_api
from .views import WatchListAPI, WatchListDetailAPI, StreamPlatformAPI, StreamPlatformDetailAPI


urlpatterns = [
    path('watchlist', WatchListAPI.as_view(), name='watchlist'),
    path('watchlist/<int:pk>', WatchListDetailAPI.as_view(), name='watchlist-detail'),
    path('latform', StreamPlatformAPI.as_view(), name='streamplatform-list'),
    path('platform/<int:pk>', StreamPlatformDetailAPI.as_view(), name='streamplatform-detail'),
    # path('list', movie_list_api, name='movie-list'),
    # path('<int:pk>', movie_detail_api, name='movie-detail'),
]