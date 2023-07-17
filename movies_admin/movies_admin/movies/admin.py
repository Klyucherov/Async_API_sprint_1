from django.contrib import admin

from .custom_filters import (CreationDateListFilter, RatingListFilter,
                             TypeListFilter)
from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    fk_name = 'film_work'


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    fk_name = 'film_work'


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'get_genres',
        'get_persons',
    )
    list_filter = (TypeListFilter, RatingListFilter, CreationDateListFilter)
    search_fields = ('title', )
    list_per_page = 25


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name', )
    list_per_page = 25
