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

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE']) # Here by default it use GET method
def movie_detail_api(request, pk):
    if request.method == 'GET':
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    if request.method == 'PUT':
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        movie = Movie.objects.get(id=pk)
        movie.delete()
        return Response({'Message': 'Movie deleted successfully'})
