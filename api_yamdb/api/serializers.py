from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class JwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=512)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
