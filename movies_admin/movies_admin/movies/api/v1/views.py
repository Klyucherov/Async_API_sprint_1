from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def persons_by_role(role):
        return ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role=role),
            distinct=True)

    def get_queryset(self):
        query = Filmwork.objects.prefetch_related(
            'genres', 'persons').values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self.persons_by_role('actor'),
            directors=self.persons_by_role('director'),
            writers=self.persons_by_role('writer'),
        )
        return query

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        cur_page = self.request.GET.get('page')

        match cur_page:
            case 'first':
                cur_page = 1
            case 'last':
                cur_page = paginator.num_pages
            case None:
                cur_page = 1

        results = paginator.get_page(cur_page)
        context = {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev": (
                results.previous_page_number() if results.has_previous()
                else None),
            "next": (
                results.next_page_number() if results.has_next()
                else None),
            'results': list(results)
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.object
