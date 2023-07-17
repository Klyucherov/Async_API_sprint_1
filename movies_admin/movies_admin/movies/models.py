import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name

    name = models.TextField(_('name'), unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name

    full_name = models.TextField(_('name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_idx',
            ),
        ]
        indexes = [
            models.Index(fields=['film_work']),
            models.Index(fields=['person']),
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title

    class FilmType(models.TextChoices):
        movie = ('movie', _('Фильм'))
        tv_show = ('tv_show', _('Шоу'))

    title = models.TextField(_('name'))
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
    )
    type = models.CharField(_('type'), max_length=7, choices=FilmType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def get_genres(self):
        return ", ".join([str(genre) for genre in self.genres.all()])
    get_genres.short_description = _('genres')

    def get_persons(self):
        return ", ".join([str(person) for person in self.persons.all()])
    get_persons.short_description = _('actors')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['creation_date', 'rating']),
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='genre_film_work_unique_idx',
            ),
        ]
        indexes = [
            models.Index(fields=['film_work']),
            models.Index(fields=['genre']),
        ]
