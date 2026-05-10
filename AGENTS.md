# AI Agent Guide for Base Django Project

## Purpose
This file helps AI coding agents quickly understand the repository, run the project, and make productive changes.

## Key Information
- Django 6.0.4 project with Django REST Framework and JWT authentication.
- API documentation is generated with `drf-yasg` and exposed at `/swagger/` and `/redoc/`.
- The main application is `user/`, which contains models, serializers, views, auth logic, and API routes.
- The default user model is configured in `base_django_project/settings.py` via `AUTH_USER_MODEL = "user.User"`.

## Run Commands
Use the project virtual environment under `venv/`.

```bash
cd d:\Users\songo\PycharmProjects\base_django_project
venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

Developer validation:

```bash
python manage.py check
python manage.py test  # if tests are added later
```

## Important Files
- `manage.py` - Django CLI entrypoint
- `requirements.txt` - Python dependencies
- `base_django_project/settings.py` - project settings, REST framework, JWT, Swagger
- `base_django_project/urls.py` - root URL configuration
- `base_django_project/swagger_inspectors.py` - custom DRF inspectors for Swagger (filters, pagination, search, ordering)
- `user/models.py` - custom user, role, and tag models
- `user/serializers.py` - request/response serializers, login/register logic
- `user/views.py` - API views (auth, user detail, tags with pagination, health check), custom `TagPagination` class
- `user/urls.py` - app-level API routes
- `user/auth.py` - custom permission classes (`IsAdmin`, `IsAuthenticationCustom`)
- `user/filters.py` - DjangoFilterBackend filter sets

## API Notes
- API base path: `/api/`
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`
- Health check endpoint: `/api/health-check/`
- Authentication uses JWT tokens; requests should include `Authorization: Bearer <token>`.

## Pagination & Query Parameters
List endpoints (e.g., `/api/tags/`) support:
- **Pagination**: `page` (default: 1) and `page_size` (default: 10, max: 100)
  - Response format: `{ "page": 1, "page_size": 10, "total_page": 5, "total_count": 50, "results": [...] }`
- **Filtering**: view-specific filter fields (check `filterset_class` in each viewset)
- **Search**: `search` param searches within `search_fields`
- **Ordering**: `ordering` param sorts by available fields (prefix with `-` for descending)

Custom pagination is defined in `TagPagination` class in `user/views.py`. To reuse for other list endpoints:
```python
class MyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        from math import ceil
        total_pages = ceil(self.page.paginator.count / self.get_page_size(self.request)) if self.page.paginator.count > 0 else 1
        return Response({
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total_page': total_pages,
            'total_count': self.page.paginator.count,
            'results': data
        })
```

## Permissions & Authentication
- `IsAuthenticated` - Any logged-in user
- `IsAdmin` - Only users with admin role (`user.roles` contains a Role with `name='admin'`)
- `AllowAny` - Public endpoints (register, login, health check)
- `TagViewSet`: GET/list requires `IsAuthenticated`; PUT/DELETE requires `IsAdmin`

## Swagger Customization
Custom inspectors are in `base_django_project/swagger_inspectors.py`:
- `CustomFilterInspector` - Displays filter fields in Swagger
- `CustomPaginationInspector` - Adds `page` and `page_size` parameters to list endpoints
- Configured in `SWAGGER_SETTINGS['DEFAULT_FILTER_INSPECTORS']` and `DEFAULT_PAGINATOR_INSPECTORS`

When adding new filter backends or paginators, update inspectors to document them in Swagger.

## Project Conventions
- Most API code lives in the `user` app.
- The project uses DRF view classes (`APIView` and `ModelViewSet`).
- Swagger is configured with `drf-yasg` and custom filter inspectors.

## Troubleshooting
- Swagger auth may require correct `Authorization` header formatting.
- Watch for absolute Windows paths in `settings.py` for `drf_yasg` templates/static dirs; these may need adjustment if the environment changes.
- If `auth/me` fails in Swagger but works in Postman, inspect header handling and `DEFAULT_AUTHENTICATION_CLASSES`.

## Guidance for Agents
- Preserve existing file structure when updating features.
- Use `manage.py check` after configuration or settings changes.
- Prefer fixes in `user/` app for auth and API behavior.
- Do not assume any extra files beyond `README.md`, `STRUCTURE.md`, and the `user/` app.
