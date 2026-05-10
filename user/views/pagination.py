from rest_framework import pagination, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from user.response import build_success_payload


class StandardizedResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response is None or getattr(response, "data", None) is None:
            return response
        if isinstance(response.data, dict) and "code" in response.data and "status" in response.data:
            return response
        if response.status_code >= 400:
            return response

        data = response.data
        message = "Success"
        metadata = None

        if isinstance(data, dict) and "data" in data:
            message = data.get("message", "Success")
            metadata = data.get("metadata")
            data = data.get("data")

        response.data = build_success_payload(data=data, message=message, code=response.status_code, metadata=metadata)
        return response


class StandardizedAPIView(StandardizedResponseMixin, APIView):
    pass


class StandardizedModelViewSet(StandardizedResponseMixin, viewsets.ModelViewSet):
    pass


class StandardizedReadOnlyModelViewSet(StandardizedResponseMixin, viewsets.ReadOnlyModelViewSet):
    pass


class TagPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        from math import ceil
        total_pages = ceil(self.page.paginator.count / self.get_page_size(self.request)) if self.page.paginator.count > 0 else 1
        metadata = {
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total_page': total_pages,
            'total_count': self.page.paginator.count,
        }
        return Response(build_success_payload(data=data, metadata=metadata))
