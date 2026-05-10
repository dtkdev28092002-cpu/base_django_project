# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate venv (Windows)
venv\Scripts\activate

# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Format
black .
isort .

# Tests
python manage.py test
```

API docs at `/swagger/` and `/redoc/` after starting the server.

## Architecture

Single Django app (`user/`) contains all models, serializers, filters, views, and URL routes. The `base_django_project/` package holds settings, root URLs, and Swagger config.

**Key quirk in settings.py:** `TEMPLATES['DIRS']` and `STATICFILES_DIRS` use hardcoded absolute paths pointing into the venv for `drf_yasg` assets. If the venv is moved or recreated, these must be updated manually.

### Response wrapping

All responses follow a unified envelope. `StandardizedResponseMixin` (in [user/views/pagination.py](user/views/pagination.py)) intercepts `finalize_response` and wraps any non-envelope response:

```json
{ "code": 200, "status": "success", "message": "...", "data": {...} }
{ "code": 400, "status": "error",   "message": "...", "error": {...} }
```

`build_success_payload` / `build_error_payload` in [user/response.py](user/response.py) construct these dicts. `custom_exception_handler` (registered in `REST_FRAMEWORK['EXCEPTION_HANDLER']`) applies the same envelope to DRF exceptions.

Paginated responses add a `metadata` key: `{ page, page_size, total_page, total_count }`.

### ViewSet pattern

Views inherit `StandardizedModelViewSet` (extends `viewsets.ModelViewSet` + `StandardizedResponseMixin`). Standard patterns used across Tag/Post/Comment:

- `get_serializer_class()` returns a `WriteSerializer` for `create`/`update`, a read serializer otherwise.
- `get_permissions()` returns `[IsAdmin()]` for `update`/`destroy`, `[IsAuthenticationCustom()]` for the rest.
- `create()` calls `serializer.save(user=request.user)` to attach the authenticated user.
- `TagPagination` is set as `pagination_class` on all list views (page_size=10, max=100).

### Authentication & permissions

JWT via `rest_framework_simplejwt`. Header: `Authorization: Bearer <token>`.

- `IsAuthenticationCustom` — checks `request.user.is_authenticated` (default permission class).
- `IsAdmin` — additionally checks `request.user.roles.filter(name='admin').exists()`.

**Note:** Admin access is role-based (`user.roles`), not Django's `is_staff`/`is_superuser`.

### Custom User model

`AUTH_USER_MODEL = "user.User"`. Login field is `email` (not `username`). The model adds `full_name`, `roles` (M2M to `Role`), `created_at`, `updated_at` on top of `AbstractUser`.

### Swagger inspectors

`base_django_project/swagger_inspectors.py` provides `CustomFilterInspector` and `CustomPaginationInspector` to expose `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`, and `TagPagination` parameters in the Swagger UI. When adding new filter backends or a different paginator, update these inspectors.

## URL structure

All API routes are under `/api/` (mounted in [base_django_project/urls.py](base_django_project/urls.py), defined in [user/urls.py](user/urls.py)):

| Prefix | ViewSet / View |
|---|---|
| `auth/register/user/`, `auth/register/admin/` | `RegisterUserView`, `RegisterAdminView` |
| `auth/login/` | `UserLoginView` |
| `auth/me/` | `UserDetailView` |
| `tags/`, `tags/<pk>/`, `tags/me/` | `TagViewSet`, `TagMeListView` |
| `posts/`, `posts/<pk>/`, `posts/me/` | `PostViewSet`, `PostMeListView` |
| `comments/`, `comments/<pk>/`, `comments/me/` | `CommentViewSet`, `CommentMeListView` |

All list endpoints support `search`, `ordering`, `page`, `page_size` query params plus resource-specific filters.
