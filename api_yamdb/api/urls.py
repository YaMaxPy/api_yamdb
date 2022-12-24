from django.urls import include, path
from rest_framework import routers
from . import views
from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet


router = routers.DefaultRouter()
router.register('users', views.UsersViewSet, basename='users_list')
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.get_confirmation_code, name='signup'),
    path('v1/auth/token/', views.get_jwt_token, name='get_token'),
    path('v1/users/me/', views.get_current_user, name='current_user'),
]
