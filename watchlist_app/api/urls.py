from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import movie_list_api, movie_detail_api
from .views import (WatchListAPI, WatchListDetailAPI, StreamPlatformAPI, StreamPlatformDetailAPI,
                    ReviewListAPI, ReviewDetailAPI, ReviewCreateAPI, PlatFormVS, UserReviewAPI, WatchListTest)


router = DefaultRouter()
router.register(r'platforms', PlatFormVS, basename='platforms')


urlpatterns = [
    path('watchlist', WatchListAPI.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchListDetailAPI.as_view(), name='watchlist-detail'),
    path('watchlist/<int:pk>/review-create', ReviewCreateAPI.as_view(), name='review-create'),
    path('watchlist/<int:pk>/review', ReviewListAPI.as_view(), name='review-list'),
    path('watchlist/review/<int:pk>', ReviewDetailAPI.as_view(), name='review-detail'),
    path('platform', StreamPlatformAPI.as_view(), name='streamplatform-list'),
    path('platform/<int:pk>', StreamPlatformDetailAPI.as_view(), name='streamplatform-detail'),
    path('list/test/', WatchListTest.as_view(), name='watchlist-test'),

    path('reviews/', UserReviewAPI.as_view(), name='user-review'),

    # path('list', movie_list_api, name='movie-list'),
    # path('<int:pk>', movie_detail_api, name='movie-detail'),
    path('', include(router.urls)),
]