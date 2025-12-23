from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import FilmWork


class MoviesListApi(BaseListView):
    model = FilmWork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get_queryset(self):
        qs = FilmWork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating').annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'persons__full_name',
                distinct=True,
                filter=Q(personfilmwork__role='actor'),
            ),
            directors=ArrayAgg(
                'persons__full_name',
                distinct=True,
                filter=Q(personfilmwork__role='director'),
            ),
            writers=ArrayAgg(
                'persons__full_name',
                distinct=True,
                filter=Q(personfilmwork__role='writer'),
            )
        )[:3]

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
