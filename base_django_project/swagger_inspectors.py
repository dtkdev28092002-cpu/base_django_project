import django_filters
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg import openapi
from drf_yasg.inspectors import FilterInspector, PaginatorInspector, NotHandled


class CustomFilterInspector(FilterInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            view = self.view
            filterset_class = getattr(view, 'filterset_class', None)
            if not filterset_class or not issubclass(filterset_class, FilterSet):
                return NotHandled

            parameters = []
            for name, filter_field in filterset_class.base_filters.items():
                param_type = openapi.TYPE_STRING
                param_format = None
                if isinstance(filter_field, django_filters.filters.BooleanFilter):
                    param_type = openapi.TYPE_BOOLEAN
                elif isinstance(filter_field, django_filters.filters.NumberFilter):
                    param_type = openapi.TYPE_NUMBER
                elif isinstance(filter_field, django_filters.filters.DateTimeFilter):
                    param_format = openapi.FORMAT_DATETIME
                elif isinstance(filter_field, django_filters.filters.DateFilter):
                    param_format = openapi.FORMAT_DATE
                elif isinstance(filter_field, django_filters.filters.TimeFilter):
                    param_format = openapi.FORMAT_TIME

                parameters.append(
                    openapi.Parameter(
                        name,
                        openapi.IN_QUERY,
                        description=str(filter_field.label or name),
                        type=param_type,
                        format=param_format,
                        required=bool(filter_field.extra.get('required', False)),
                    )
                )

            return parameters

        if isinstance(filter_backend, SearchFilter):
            if getattr(self.view, 'search_fields', None):
                return [
                    openapi.Parameter(
                        'search',
                        openapi.IN_QUERY,
                        description='Search within fields: %s' % ', '.join(self.view.search_fields),
                        type=openapi.TYPE_STRING,
                        required=False,
                    )
                ]
            return NotHandled

        if isinstance(filter_backend, OrderingFilter):
            if getattr(self.view, 'ordering_fields', None):
                return [
                    openapi.Parameter(
                        'ordering',
                        openapi.IN_QUERY,
                        description='Order by fields: %s (prefix with - for descending)' % ', '.join(self.view.ordering_fields),
                        type=openapi.TYPE_STRING,
                        required=False,
                    )
                ]
            return NotHandled

        return NotHandled


class CustomPaginationInspector(PaginatorInspector):
    def get_paginator_parameters(self, paginator):
        parameters = []
        if hasattr(paginator, 'page_size_query_param') and paginator.page_size_query_param:
            parameters.append(
                openapi.Parameter(
                    'page',
                    openapi.IN_QUERY,
                    description='Page number',
                    type=openapi.TYPE_INTEGER,
                    required=False,
                )
            )
            parameters.append(
                openapi.Parameter(
                    paginator.page_size_query_param,
                    openapi.IN_QUERY,
                    description='Number of items per page (max: %d)' % paginator.max_page_size,
                    type=openapi.TYPE_INTEGER,
                    required=False,
                )
            )
        return parameters
