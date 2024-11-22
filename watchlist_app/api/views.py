from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieSerializer
from watchlist_app.models import Movie


class MovieListAPI(APIView):
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
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
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
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPI(APIView):
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
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
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
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
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
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response({'Message': 'Movie deleted successfully'}, status=status.HTTP_200_OK)



# @api_view(['GET', 'POST']) # Here by default it use GET method
# def movie_list_api(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE']) # Here by default it use GET method
# def movie_detail_api(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
#
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExist:
#             return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response({'Message': 'Movie deleted successfully'}, status=status.HTTP_200_OK)
