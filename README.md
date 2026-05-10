# Base Django Project

A starter Django project with Django REST Framework (DRF), JWT authentication, and Swagger API documentation setup. This project serves as a foundation for building RESTful APIs with user authentication and comprehensive API documentation.

## Features

- Django 6.0.4
- Django REST Framework for building APIs
- JWT authentication using djangorestframework-simplejwt
- **Swagger/OpenAPI documentation** with drf-yasg
- PostgreSQL support (via psycopg2-binary)
- Code formatting with Black and isort
- Environment variable management with python-decouple
- SQLite database for development
- Tag management API endpoints (example implementation)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd base_django_project
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the Django admin at `http://127.0.0.1:8000/admin/`
- **API Documentation (Swagger UI)**: `http://127.0.0.1:8000/swagger/`
- **API Documentation (ReDoc)**: `http://127.0.0.1:8000/redoc/`
- **Raw OpenAPI JSON**: `http://127.0.0.1:8000/swagger.json`
- API endpoints are available under `/api/` path
- Current API endpoints: Tag management (GET, POST, PUT, DELETE operations)

## API Endpoints

The project includes example Tag management endpoints with comprehensive query parameter support:

### Available Query Parameters

- `page` - Page number (default: 1)
- `page_size` - Number of items per page (default: 10, max: 100)
- `name` - Filter tags by name (case-insensitive partial match)
- `created_after` - Filter tags created after date (ISO format: YYYY-MM-DDTHH:MM:SS)
- `created_before` - Filter tags created before date (ISO format: YYYY-MM-DDTHH:MM:SS)
- `search` - Search within tag names
- `ordering` - Order results by field (prefix with `-` for descending)
  - Available fields: `name`, `created_at`, `updated_at`
  - Default: `-created_at` (newest first)

### Endpoint Examples

- `GET /api/tags/` - List all tags (paginated)
- `GET /api/tags/?page=1&page_size=20` - List tags with custom page size
- `GET /api/tags/?name=python` - Filter tags containing "python"
- `GET /api/tags/?search=django&ordering=name` - Search and sort by name
- `GET /api/tags/?created_after=2024-01-01T00:00:00` - Filter by creation date
- `POST /api/tags/` - Create a new tag (requires authentication)
- `GET /api/tags/{id}/` - Retrieve a specific tag (requires authentication)
- `PUT /api/tags/{id}/` - Update a specific tag (requires admin role)
- `DELETE /api/tags/{id}/` - Delete a specific tag (requires admin role)

### Pagination Response Format

List endpoints return paginated responses:
```json
{
  "page": 1,
  "page_size": 10,
  "total_page": 5,
  "total_count": 50,
  "results": [...]
}
```

All endpoints are documented in the Swagger UI and can be tested interactively with query parameters.

## Using Swagger Documentation

The Swagger UI provides an interactive interface to explore and test your API:

1. **Access Swagger UI**: Navigate to `http://127.0.0.1:8000/swagger/`

2. **Explore Endpoints**:
   - Click on any endpoint to expand it
   - View request/response schemas
   - See parameter requirements

3. **Test Endpoints**:
   - Click the "Try it out" button
   - Fill in required parameters
   - Click "Execute" to send the request
   - View the response directly in the interface

4. **Authentication** (if implemented):
   - Use the "Authorize" button for JWT tokens
   - Enter your authentication credentials

5. **Alternative Views**:
   - **ReDoc**: `http://127.0.0.1:8000/redoc/` - Clean, mobile-friendly documentation
   - **Raw JSON**: `http://127.0.0.1:8000/swagger.json` - OpenAPI specification

## API Documentation Setup

This project uses `drf-yasg` (Yet Another Swagger Generator for Django Rest Framework) to provide interactive API documentation.

### Dependencies

Add to `requirements.txt`:

```txt
drf-yasg==1.21.6
django-filter==24.3  # For advanced filtering
coreapi==2.3.3  # Required for django-filter schema generation
setuptools<82  # Required for pkg_resources compatibility
```

### Django Settings Configuration

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_filters',  # For filtering
    'drf_yasg',  # For API documentation
]
```

Configure templates and static files in `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Update this path to match your virtual environment
            r"D:\Users\songo\PycharmProjects\base_django_project\venv\Lib\site-packages\drf_yasg\templates",
        ],
        'APP_DIRS': True,
        # ... rest of template config
    },
]

STATICFILES_DIRS = [
    # Update this path to match your virtual environment
    r"D:\Users\songo\PycharmProjects\base_django_project\venv\Lib\site-packages\drf_yasg\static",
]
```

**Note**: Update the paths above to match your virtual environment location. For Linux/macOS, the path would be something like `/path/to/venv/lib/python3.x/site-packages/drf_yasg/`.

### Swagger Settings Configuration

Add Swagger settings to disable automatic filter inspection (to avoid coreapi dependency issues):

```python
# Swagger settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_FILTER_INSPECTORS': [],  # Disable automatic filter inspection
}
```

### URL Configuration

Add to main `urls.py`:

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Swagger documentation for your API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # ... other URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
```

### Troubleshooting

- **TemplateDoesNotExist**: Ensure the drf-yasg templates directory is in `TEMPLATES['DIRS']`
- **Static files 404**: Ensure the drf-yasg static directory is in `STATICFILES_DIRS`
- **pkg_resources error**: Use `setuptools<82` for compatibility with Python 3.14+
- **coreapi must be installed error**: Add `'DEFAULT_FILTER_INSPECTORS': []` to `SWAGGER_SETTINGS` to disable automatic filter parameter inspection
- **Query parameters not showing in Swagger**: Ensure manual parameters are defined using `@swagger_auto_schema` decorators with `manual_parameters`

## Development

- Format code with Black: `black .`
- Sort imports with isort: `isort .`

## License

This project is open-source. Please check the license file for details.
