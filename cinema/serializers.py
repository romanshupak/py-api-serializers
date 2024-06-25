from rest_framework import serializers

from cinema.models import Genre, CinemaHall, Actor, Movie, MovieSession


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class MovieSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True)
    # actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors")


class MovieRetrieveSerializer(MovieSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)


class MovieListSerializer(MovieSerializer):
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class MovieSessionSerializer(serializers.ModelSerializer):
    # movie = MovieListSerializer()
    # cinema_hall = CinemaHallSerializer()

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionListSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(
        source="movie.title",
        read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity",
        read_only=True
    )
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name",
        read_only=True
    )

    class Meta:
        model = MovieSession
        fields = (
            "id", "show_time",
            "movie_title", "cinema_hall_name",
            "cinema_hall_capacity"
        )


class MovieSessionRetrieveSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer()
    cinema_hall = CinemaHallSerializer()

    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")
