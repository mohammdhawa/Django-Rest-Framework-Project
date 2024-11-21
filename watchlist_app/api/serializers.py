from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new Movie instance using the validated data.

        Args:
            validated_data (dict): The data that has been validated and
                                   is ready for creating a new Movie object.

        Returns:
            Movie: The newly created Movie instance.
        """
        movie = Movie.objects.create(**validated_data)
        return movie
