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

The project includes example Tag management endpoints:

- `GET /api/tags/` - List all tags
- `POST /api/tags/` - Create a new tag
- `GET /api/tags/{id}/` - Retrieve a specific tag
- `PUT /api/tags/{id}/` - Update a specific tag
- `DELETE /api/tags/{id}/` - Delete a specific tag

All endpoints are documented in the Swagger UI and can be tested interactively.

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
setuptools<82  # Required for pkg_resources compatibility
```

### Django Settings Configuration

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'drf_yasg',
]
```

Configure templates and static files in `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Windows
            r'C:\path\to\your\venv\Lib\site-packages\drf_yasg\templates',
            # macOS/Linux
            '/path/to/your/venv/lib/python3.x/site-packages/drf_yasg/templates',
        ],
        'APP_DIRS': True,
        # ... rest of template config
    },
]

STATICFILES_DIRS = [
    # Windows
    r'C:\path\to\your\venv\Lib\site-packages\drf_yasg\static',
    # macOS/Linux
    '/path/to/your/venv/lib/python3.x/site-packages/drf_yasg/static',
]
```

**Note**: Replace `python3.x` with your actual Python version (e.g., `python3.11`) and update the venv path to match your virtual environment location.

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

## Development

- Format code with Black: `black .`
- Sort imports with isort: `isort .`

## License

This project is open-source. Please check the license file for details.
