from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles'
    )
    rating = models.IntegerField(
        null=True,
        default=None
    )
    year = models.IntegerField(
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
