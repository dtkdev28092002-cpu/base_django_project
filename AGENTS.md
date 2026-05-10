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
- `base_django_project/swagger.py` - Swagger schema and inspector configuration
- `user/models.py` - custom user and tag models
- `user/serializers.py` - request/response serializers, login/register logic
- `user/views.py` - API views for auth, user detail, tags, health check
- `user/urls.py` - app-level API routes

## API Notes
- API base path: `/api/`
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`
- Health check endpoint is provided in `user/urls.py` and may be exposed at `/api/`.
- Authentication uses JWT tokens; requests should include `Authorization: Bearer <token>`.

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
