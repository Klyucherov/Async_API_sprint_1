from datetime import date, datetime

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class RatingListFilter(admin.SimpleListFilter):
    title = _('rating')
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0-10')),
            ('1', _('10-20')),
            ('2', _('20-30')),
            ('3', _('30-40')),
            ('4', _('40-50')),
            ('5', _('50-60')),
            ('6', _('60-70')),
            ('7', _('70-80')),
            ('8', _('80-90')),
            ('9', _('90-100')),
        )

    def queryset(self, request, queryset):
        if self.value():
            low_level = int(self.value()) * 10
            high_level = low_level + 10
            return queryset.filter(
                rating__gte=low_level,
                rating__lte=high_level,
            )


class CreationDateListFilter(admin.SimpleListFilter):
    title = _('creation_date')
    parameter_name = 'creation_date'
    dates = tuple(
        (cur_year for cur_year in range(1980, datetime.now().year + 10, 10)),
    )

    def lookups(self, request, model_admin):
        return (
            ('0', _('<1980')),
            ('1', _('1980-1990')),
            ('2', _('1990-2000')),
            ('3', _('2000-2010')),
            ('4', _('2010-2020')),
            ('5', _('2020-')),
        )

    def queryset(self, request, queryset):
        match self.value():
            case '0':
                return queryset.filter(
                    creation_date__lte=date(year=self.dates[0], month=1, day=1),
                )
            case '5':
                return queryset.filter(
                    creation_date__gte=date(year=self.dates[5], month=1, day=1),
                )
            case '1' | '2' | '3' | '4':
                choice = int(self.value())

                return queryset.filter(
                    creation_date__gte=date(
                        year=self.dates[choice - 1],
                        month=1,
                        day=1,
                    ),
                    creation_date__lte=date(
                        year=self.dates[choice],
                        month=1,
                        day=1,
                    ),
                )


class TypeListFilter(admin.SimpleListFilter):
    title = _('type')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('movie', _('Фильм')),
            ('show', _('Шоу')),
        )

    def queryset(self, request, queryset):
        match self.value():
            case 'movie':
                return queryset.filter(type='movie')
            case 'tv_show':
                return queryset.filter(type='tv_show')
