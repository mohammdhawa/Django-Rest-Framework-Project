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

    def update(self, instance, validated_data):
        """
        Update and return an existing Movie instance with validated data.

        This method updates the fields of the provided Movie instance
        with the values from validated_data. If a field is not present
        in validated_data, the current value of that field remains unchanged.

        Args:
            instance (Movie): The existing Movie instance to be updated.
            validated_data (dict): The data that has been validated and
                                   contains the updates for the Movie object.

        Returns:
            Movie: The updated Movie instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()

        return instance

    def validate_name(self, value):
        """
        Validate the 'name' field of the Movie instance.

        This method ensures that the 'name' field meets the required
        criteria before the data is processed further. Specifically,
        it checks that the name has a minimum length of 2 characters.
        If the validation fails, a ValidationError is raised.

        Args:
            value (str): The value of the 'name' field provided for validation.

        Returns:
            str: The validated 'name' value if it meets the criteria.

        Raises:
            serializers.ValidationError: If the 'name' is less than 2 characters long.
        """
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        else:
            return value

