from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieSerializer
from watchlist_app.models import Movie


@api_view(['GET', 'POST']) # Here by default it use GET method
def movie_list_api(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) # Here by default it use GET method
def movie_detail_api(request, pk):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    if request.method == 'PUT':
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'message': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response({'Message': 'Movie deleted successfully'}, status=status.HTTP_200_OK)
