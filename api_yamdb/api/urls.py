from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet,  GenreViewSet

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
