from rest_framework import serializers

from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'year', 'description', 'genre', 'category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre