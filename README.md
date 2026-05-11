# Base Django Project

A starter Django REST Framework project with JWT authentication, role-based permissions, Swagger documentation, and a standardized API response envelope.

## Quick Start

```bash
git clone <repository-url>
cd base_django_project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# Install dependencies and apply migrations
pip install -r requirements.txt
python manage.py migrate

# Run the development server
python manage.py runserver
```

API docs: `http://127.0.0.1:8000/swagger/`

## Features

- Django 6.0.4 + Django REST Framework
- JWT authentication (`djangorestframework-simplejwt`) — 1-day access / 30-day refresh tokens
- Role-based permissions (`user` / `admin` roles via M2M, not `is_staff`)
- Standardized response envelope for all endpoints (success + error)
- Swagger/OpenAPI docs via `drf-yasg` (`/swagger/`, `/redoc/`)
- Filtering, search, and ordering on all list endpoints (`django-filter`)
- Email utilities (plain text and HTML template)
- Environment config via `python-decouple`
- PostgreSQL support (SQLite default for development)

## Installation

1. Clone and enter the repo:

   ```bash
   git clone <repository-url>
   cd base_django_project
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (copy from the example below):

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   # Optional — omit to use SQLite
   DATABASE_URL=postgres://user:pass@localhost:5432/dbname
   # Optional — for email sending
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=user@example.com
   EMAIL_HOST_PASSWORD=password
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the dev server:

   ```bash
   python manage.py runserver
   ```

**Note:** `settings.py` has hardcoded absolute paths for `drf_yasg` templates and static files pointing into the venv. If you move or recreate the venv, update `TEMPLATES['DIRS']` and `STATICFILES_DIRS` in `settings.py` to point to the new location (e.g., `venv/lib/python3.x/site-packages/drf_yasg/`).

## API Endpoints

All routes are under `/api/`. Full interactive docs at `http://127.0.0.1:8000/swagger/`.

### Auth

| Method | Path                        | Description                                     |
| ------ | --------------------------- | ----------------------------------------------- |
| POST   | `/api/auth/register/user/`  | Register a regular user                         |
| POST   | `/api/auth/register/admin/` | Register an admin user                          |
| POST   | `/api/auth/login/`          | Login — returns `access` + `refresh` JWT tokens |
| GET    | `/api/auth/me/`             | Get current user profile                        |

### Tags / Posts / Comments

Each resource follows the same pattern:

| Method    | Path                    | Auth     | Permission                           |
| --------- | ----------------------- | -------- | ------------------------------------ |
| GET       | `/api/{resource}/`      | Required | Any authenticated                    |
| POST      | `/api/{resource}/`      | Required | Any authenticated                    |
| GET       | `/api/{resource}/{id}/` | Required | Any authenticated                    |
| PUT/PATCH | `/api/{resource}/{id}/` | Required | Admin only                           |
| DELETE    | `/api/{resource}/{id}/` | Required | Admin only                           |
| GET       | `/api/{resource}/me/`   | Required | Any authenticated (own records only) |

Resources: `tags`, `posts`, `comments`.

### Authentication header

```
Authorization: Bearer <access_token>
```

## Response Format

All endpoints return a unified envelope:

```json
{ "code": 200, "status": "success", "message": "...", "data": { ... } }
{ "code": 400, "status": "error",   "message": "...", "error": { ... } }
```

Paginated list responses include a `metadata` key:

```json
{
  "code": 200,
  "status": "success",
  "message": "...",
  "data": [...],
  "metadata": { "page": 1, "page_size": 10, "total_page": 5, "total_count": 50 }
}
```

## Query Parameters

All list endpoints support:

| Parameter   | Description                            |
| ----------- | -------------------------------------- |
| `page`      | Page number (default: 1)               |
| `page_size` | Items per page (default: 10, max: 100) |
| `search`    | Full-text search                       |
| `ordering`  | Field name, prefix `-` for descending  |

Resource-specific filters:

| Resource | Filter params                                 |
| -------- | --------------------------------------------- |
| Tags     | `name` (partial match)                        |
| Posts    | `title`, `content`, `author_email`, `tag_ids` |
| Comments | `content`, `author_email`, `post_title`       |

## Development

```bash
# Update requirements.txt after installing new packages
pip freeze > requirements.txt

# Format
black .
isort .

# Run all tests
python manage.py test

# Run a specific test
python manage.py test user.tests.TestClassName.test_method_name

# Send email via CLI
python manage.py send_email --to user@example.com --subject "Hi" --body "Hello"
python manage.py send_email --to user@example.com --subject "Hi" --template emails/base.html --context '{"name": "World"}'
```

## License

This project is open-source. Please check the license file for details.
