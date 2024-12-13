from urllib import request

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, generics
from rest_framework import viewsets

from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review


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


class PlatFormVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer




class ReviewCreateAPI(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(id=pk)

        user = self.request.user
        review_queryset = Review.objects.filter(review_user=user, watchlist=movie)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        serializer.save(watchlist=movie, review_user=user)


class ReviewListAPI(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(watchlist__id=self.kwargs['pk'])
        return queryset




class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



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
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAPI(APIView):
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
        movie.delete()
        return Response({'Message': 'WatchList deleted successfully'}, status=status.HTTP_200_OK)


class StreamPlatformAPI(APIView):
    def get(self, request):
        streamplatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatform, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': "Streamplatform Not Found"}, status=status.HTTP_404_NOT_FOUND)

        streamplatform.delete()
        return Response({'Message': 'StreamPlatform deleted successfully'}, status=status.HTTP_200_OK)