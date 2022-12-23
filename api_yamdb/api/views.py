from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .pagination import UsersPagination
from .permissions import IsAdmin

User = get_user_model()
EMAIL = 'admin@mail.com'


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_confirmation_code(request):
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        user = User.objects.get(username=request.data.get('username'),
                                email=request.data.get('email'))
        code = default_token_generator.make_token(user)
        send_mail('Confirmation code',
                  f'Confirmation code: {code}',
                  EMAIL,
                  [request.data.get('email')],
                  fail_silently=False)
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = serializers.ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if serializer.validated_data['username'] == 'me':
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = get_object_or_404(User,
                                 username=serializer.data.get('username'))
        code = default_token_generator.make_token(user)
        send_mail('Confirmation code',
                  f'Confirmation code: {code}',
                  EMAIL,
                  [serializer.data.get('email')],
                  fail_silently=False)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_jwt_token(request):
    serializer = serializers.JwtTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User,
                                 username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            context = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = UsersPagination
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('=username',)
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes((permissions.IsAuthenticated,))
def get_current_user(request):
    if request.method == 'GET':
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)
    obj = User.objects.get(id=request.user.id)
    serializer = serializers.UserSerializer(obj,
                                            data=request.data,
                                            partial=True)
    if serializer.is_valid(raise_exception=True):
        if 'role' in serializer.validated_data:
            serializer.validated_data.pop('role')
            serializer.save()
            return Response(serializer.data)
        serializer.save()
        return Response(serializer.data)
