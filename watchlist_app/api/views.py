from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieSerializer
from watchlist_app.models import Movie


@api_view() # Here by default it use GET method
def movie_list_api(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)


@api_view() # Here by default it use GET method
def movie_detail_api(request, pk):
    movie = Movie.objects.get(id=pk)
    serializer = MovieSerializer(movie)

    return Response(serializer.data)
