from urllib import request

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly

from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.throttling import ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from watchlist_app.api.pagination import WatchlistPagination, WatchListLimitOffsetPagination, WatchListCursorPagination


# class PlatFormVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReviewAPI(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)



class PlatFormVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # permission_classes = [AdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ReviewCreateAPI(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user:
            pk = self.kwargs['pk']
            movie = WatchList.objects.get(id=pk)

            user = self.request.user
            review_queryset = Review.objects.filter(review_user=user, watchlist=movie)

            if review_queryset.exists():
                return Response({'message': "You have already reviewed this movie"}, status=status.HTTP_400_BAD_REQUEST)

            if movie.number_rating == 0:
                movie.avg_rating = serializer.validated_data['rating']
            else:
                movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

            movie.number_rating = movie.number_rating + 1
            movie.save()

            if serializer.is_valid():
                serializer.save(watchlist=movie, review_user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class ReviewListAPI(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(watchlist__id=self.kwargs['pk'])
        return queryset


class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'



# class ReviewDetailAPI(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =  ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class WatchListAPI(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self, request, format=None):
        """
        Handles GET requests for the MovieListAPI.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            format (str, optional): Specifies the format of the response
                                    (e.g., JSON, XML). Defaults to None.

        Returns:
            Response: A Response object containing serialized movie data
                      and an HTTP 200 OK status.

        Description:
        - Retrieves all movie records from the database using the Movie model.
        - Serializes the queryset using the MovieSerializer with `many=True`
          to handle multiple objects.
        - Returns the serialized data in the response, ensuring it is formatted
          as per the API's standards.
        """
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Handles POST requests for the MovieListAPI.

        Args:
            request (HttpRequest): The incoming HTTP request object containing
                                   the data for the new movie to be created.
            format (str, optional): Specifies the format of the request
                                    (e.g., JSON, XML). Defaults to None.

        Returns:
            Response: A Response object containing:
                - Serialized data of the newly created movie and an HTTP 201
                  Created status if the data is valid and saved successfully.
                - Validation errors and an HTTP 400 Bad Request status if the
                  data is invalid.

        Description:
        - Uses the MovieSerializer to validate and deserialize the input data
          from the request.
        - If the data is valid, saves the new movie instance to the database.
        - Returns the serialized data for the created movie with a success status.
        - If validation fails, returns error details with a bad request status.
        """
        if request.user.is_superuser:
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class WatchListDetailAPI(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self, request, pk):
        """
        Handles GET requests to retrieve details of a specific movie.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            pk (int): The primary key (ID) of the movie to retrieve.

        Returns:
            Response:
                - A Response object with serialized movie data and HTTP 200 OK
                  status if the movie exists.
                - A Response object with an error message and HTTP 404 Not Found
                  status if the movie does not exist.

        Description:
        - Attempts to retrieve a movie by its primary key (ID) from the database.
        - If found, serializes the movie and returns the data in the response.
        - If the movie does not exist, returns an error message with a 404 status.
        """
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'message': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Handles PUT requests to update details of a specific movie.

        Args:
            request (HttpRequest): The incoming HTTP request object containing
                                   the updated movie data.
            pk (int): The primary key (ID) of the movie to update.

        Returns:
            Response:
                - A Response object with serialized updated movie data and HTTP 200 OK
                  status if the movie exists and the update is successful.
                - A Response object with an error message and HTTP 404 Not Found
                  status if the movie does not exist.
                - A Response object with validation errors and HTTP 400 Bad Request
                  status if the input data is invalid.

        Description:
        - Attempts to retrieve the movie by its primary key (ID).
        - If found, deserializes and validates the updated data using MovieSerializer.
        - If the data is valid, updates the movie in the database and returns the
          updated data in the response.
        - If the movie does not exist, returns an error message with a 404 status.
        - If validation fails, returns validation error details with a 400 status.
        """
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'message': "WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove a specific movie from the database.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            pk (int): The primary key (ID) of the movie to delete.

        Returns:
            Response:
                - A Response object with a success message and HTTP 200 OK status
                  if the movie is deleted successfully.
                - A Response object with an error message and HTTP 404 Not Found
                  status if the movie does not exist.

        Description:
        - Attempts to retrieve the movie by its primary key (ID).
        - If the movie exists, deletes it from the database and returns a success message.
        - If the movie does not exist, returns an error message with a 404 status.
        """
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'message': "WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            movie.delete()
            return Response({'Message': 'WatchList deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class StreamPlatformAPI(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        streamplatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatform, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser:
            serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class StreamPlatformDetailAPI(APIView):
    def get(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': "Streamplatform Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streamplatform, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': "Streamplatform Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(streamplatform, data=request.data, context={'request': request})
        if request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': "Streamplatform Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            streamplatform.delete()
            return Response({'Message': 'StreamPlatform deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class WatchListTest(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['active']
    search_fields = ['title', 'storyline', 'platform__name']
    ordering_fields = ['avg_rating', 'number_rating']
    pagination_class = WatchListCursorPagination

