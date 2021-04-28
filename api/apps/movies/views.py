from django.db import transaction

from rest_framework.views import APIView
from rest_framework.exceptions import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.movies.serializers import (
    MovieSerializer,
    MovieRatingSerializer,
    PostMovieRatingSerializer,
    UpdateRatingSerializer,
    GetMovieRatingsSerializer,
)
from apps.common.model_loaders import (
    get_movie_model,
    get_genre_model,
    get_user_model,
    get_comment_model,
    get_rating_model,
)
from apps.common.responses import ApiMessageResponse
from apps.common.permissions import CustomPermission


class MovieItem(APIView):
    def get(self, request, movie_id):
        Movie = get_movie_model()
        try:
            movie = Movie.get_movie_with_id(movie_id)
            movie_serializer = MovieSerializer(
                movie, context={"request": request}
            )
            return Response(movie_serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return ApiMessageResponse(
                "Movie not found", status=status.HTTP_404_NOT_FOUND
            )


class MovieRatings(APIView):

    permission_classes = (CustomPermission,)

    def get(self, request, movie_id):
        request_data = self._get_request_data(request, movie_id)

        serializer = GetMovieRatingsSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        movie_id = data.get("movie_id")

        Movie = get_movie_model()
        movie_ratings = Movie.get_ratings_with_movie_id(movie_id=movie_id)
        movie_ratings_serializer = MovieRatingSerializer(
            movie_ratings, many=True, context={"request": request}
        )
        return Response(
            movie_ratings_serializer.data, status=status.HTTP_200_OK
        )

    def post(self, request, movie_id):
        request_data = self._get_request_data(request, movie_id)

        serializer = PostMovieRatingSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        movie_id = data.get("movie_id")
        rating = data.get("rating")

        user = request.user

        with transaction.atomic():
            movie_rating = user.rating_movie_with_id(
                movie_id=movie_id, user=user, rating=rating
            )

        movie_rating_serializer = MovieRatingSerializer(
            movie_rating, context={"request": request}
        )
        return Response(
            movie_rating_serializer.data, status=status.HTTP_201_CREATED
        )

    def _get_request_data(self, request, movie_id):
        request_data = request.data.copy()
        query_params = request.query_params.dict()
        request_data.update(query_params)
        request_data["movie_id"] = movie_id
        return request_data


class RatingItem(APIView):

    permission_classes = (CustomPermission,)

    def get(self, request, rating_id):
        Rating = get_rating_model()
        try:
            movie = Rating.get_rating_with_id(rating_id)
            movie_serializer = MovieRatingSerializer(
                movie, context={"request": request}
            )
            return Response(movie_serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return ApiMessageResponse(
                "Rating not found", status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, movie_id, movie_rating_id):
        return

    def _get_request_data(self, request, movie_id, rating_id):
        request_data = request.data.copy()
        query_params = request.query_params.dict()
        request_data.update(query_params)
        request_data["rating_id"] = rating_id
        return request_data
