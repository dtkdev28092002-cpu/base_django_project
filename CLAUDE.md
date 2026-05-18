# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows

# Dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Format
black .
isort .

# Tests (all / single)
python manage.py test
python manage.py test user.tests.TestClassName.test_method_name

# Update requirements after installing packages
pip freeze > requirements.txt

# Management commands
python manage.py say_hello
python manage.py send_email --to user@example.com --subject "Hi" --body "Hello"
python manage.py send_email --to user@example.com --subject "Hi" --template emails/base.html --context '{"name": "World"}'
# --to accepts multiple emails; requires either --body or --template
```

API docs at `/swagger/` and `/redoc/` after starting the server.

## Architecture

Single Django app (`user/`) contains all models, serializers, filters, views, and URL routes. The `base_django_project/` package holds settings, root URLs, and Swagger config.

**Key quirk in settings.py:** `TEMPLATES['DIRS']` and `STATICFILES_DIRS` use hardcoded absolute paths pointing into the venv for `drf_yasg` assets. If the venv is moved or recreated, update `SWAGGER_DIR` and `STATIC_DIR` in `.env`.

**Environment config** uses `python-decouple` (reads from `.env`). Key vars: `SECRET_KEY`, `DEBUG`, `DATABASE_URL` (defaults to SQLite), `EMAIL_HOST`/`EMAIL_PORT`/`EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD`.

### Models

All models live in `user/models/` (one file per model, re-exported from `user/models/__init__.py`):

- `User` — extends `AbstractUser`, email is the login field (`USERNAME_FIELD = 'email'`, `REQUIRED_FIELDS = ['username']`), adds `full_name`, `roles` (M2M → `Role`), `created_at`, `updated_at`.
- `Role` — name choices `user`/`admin` (`Role.ROLE_USER`, `Role.ROLE_ADMIN` constants). Admin registration assigns both roles.
- `Tag` — optional `user` FK (owner), M2M with `Post`.
- `Post` — `author` FK to User, M2M `tags`, `title`/`content`.
- `Comment` — `author` FK, `post` FK, self-referential `parent` FK (`related_name='replies'`) for threaded replies.

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

- `get_serializer_class()` returns a `*WriteSerializer` for `create`/`update`, a read serializer otherwise.
- Read serializers nest related objects (e.g., full `UserSerializer` for `author`); write serializers accept IDs (e.g., `tag_ids` array). `PostWriteSerializer` handles `tags.set()` inside its own `create()`/`update()`.
- `get_permissions()` returns `[IsAdmin()]` for `update`/`destroy`, `[IsAuthenticationCustom()]` for the rest.
- `create()` calls `serializer.save(author=request.user)` or `serializer.save(user=request.user)` to attach the authenticated user — this is done in the ViewSet, not inside the serializer.
- `PaginationData` is set as `pagination_class` on all list views (page_size=10, max=100).
- Each resource has a `*MeListView` (e.g., `TagMeListView`) that filters the queryset to `request.user`'s own records.

### Serializers

Two serializers exist for `User`:
- `UserSerializer` — full read serializer with nested `roles`; used inside other read serializers (Tag, Post, Comment).
- `UserDetailSerializer` — used for `GET /auth/me/`; marks `email` and `username` as read-only to prevent updates through that endpoint.

`LoginSerializer.response()` generates and returns `access_token` / `refresh_token` via `RefreshToken.for_user()`. Requires `request` in serializer context.

### Filters

Each resource has a filter class in `user/filters/`:

- `TagFilter`: `name` (icontains)
- `PostFilter`: `title`, `content`, `author_email` (FK traversal), `tag_ids` (`ModelMultipleChoiceFilter` on M2M)
- `CommentFilter`: `content`, `author_email`, `post_title` (FK traversal)

All ViewSets use `DjangoFilterBackend` + `SearchFilter` + `OrderingFilter`.

### Authentication & permissions

JWT via `rest_framework_simplejwt`. Header: `Authorization: Bearer <token>`. Access tokens expire in 1 day, refresh tokens in 30 days.

- `IsAuthenticationCustom` — checks `request.user.is_authenticated` (default permission class).
- `IsAdmin` — additionally checks `request.user.roles.filter(name='admin').exists()`.

**Note:** Admin access is role-based (`user.roles`), not Django's `is_staff`/`is_superuser`. Both `RegisterUserView` and `RegisterAdminView` are `AllowAny`.

### Email utilities

`user/email.py` provides `send_plain_email(to, subject, body)` and `send_template_email(to, subject, template_name, context)`. The `SendEmailSerializer` pre-validates that all recipient emails exist in the User table before sending.

`SendEmailView` (POST `/api/emails/send/`) requires admin role and always renders `emails/base.html`, merging the `body` field and any extra `context` keys into the template. The template supports `{{ name }}` (optional greeting), `{{ body }}`, and `{{ action_url }}` (optional CTA button).

### Swagger inspectors

`base_django_project/swagger_inspectors.py` provides `CustomFilterInspector` and `CustomPaginationInspector` to expose `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`, and `PaginationData` parameters in the Swagger UI. When adding new filter backends or a different paginator, update these inspectors.

## URL structure

All API routes are under `/api/` (mounted in [base_django_project/urls.py](base_django_project/urls.py), defined in [user/urls.py](user/urls.py)):

| Prefix                                        | ViewSet / View                          |
| --------------------------------------------- | --------------------------------------- |
| `auth/register/user/`, `auth/register/admin/` | `RegisterUserView`, `RegisterAdminView` |
| `auth/login/`                                 | `UserLoginView`                         |
| `auth/me/`                                    | `UserDetailView`                        |
| `tags/`, `tags/<pk>/`, `tags/me/`             | `TagViewSet`, `TagMeListView`           |
| `posts/`, `posts/<pk>/`, `posts/me/`          | `PostViewSet`, `PostMeListView`         |
| `comments/`, `comments/<pk>/`, `comments/me/` | `CommentViewSet`, `CommentMeListView`   |
| `emails/send/`                                | `SendEmailView`                         |

Root `/` serves a health check (`{ status: "ok" }`). All list endpoints support `search`, `ordering`, `page`, `page_size` query params plus resource-specific filters.

## Tests

`user/tests.py` is currently empty — no tests exist yet.
