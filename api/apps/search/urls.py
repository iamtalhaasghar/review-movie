from django.urls import include, re_path
from rest_framework_extensions.routers import ExtendedDefaultRouter
from apps.search.views import MovieDocumentView


router = ExtendedDefaultRouter()
movies = router.register(
    "movies",
    MovieDocumentView,
    basename="movie-document",
)


urlpatterns = [
    re_path("", include(router.urls)),
]
