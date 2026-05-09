# Base Django Project

A starter Django project with Django REST Framework (DRF) and JWT authentication setup. This project serves as a foundation for building RESTful APIs with user authentication.

## Features

- Django 6.0.4
- Django REST Framework for building APIs
- JWT authentication using djangorestframework-simplejwt
- PostgreSQL support (via psycopg2-binary)
- Code formatting with Black and isort
- Environment variable management with python-decouple
- SQLite database for development

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
- API endpoints can be added in the `user` app or additional apps

## Project Structure

- `base_django_project/`: Main project settings and configuration
- `user/`: User-related models, views, and URLs (currently empty, ready for customization)
- `db.sqlite3`: SQLite database file
- `manage.py`: Django management script
- `requirements.txt`: Python dependencies

## Configuration

- Database: Configured for SQLite in development. Update `settings.py` for production databases.
- Authentication: JWT tokens for API authentication.
- Environment variables: Use `python-decouple` for sensitive settings.

## Development

- Format code with Black: `black .`
- Sort imports with isort: `isort .`

## License

This project is open-source. Please check the license file for details.
