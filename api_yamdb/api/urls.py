from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UsersViewSet, basename='users_list')
urlpatterns = [
    path('v1/auth/signup/', views.get_confirmation_code, name='signup'),
    path('v1/auth/token/', views.get_jwt_token, name='get_token'),
    path('v1/users/me/', views.get_current_user, name='current_user'),
    path('v1/', include(router.urls))
]
