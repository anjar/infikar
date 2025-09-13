# Infikar Development Container

This directory contains the configuration for the Infikar development container, which provides a complete development environment with all necessary services.

## What's Included

### Services
- **Django Web App**: Python 3.11 with Poetry
- **Redis**: For caching and session storage
- **MySQL 8.0**: Database server
- **Node.js 18**: For frontend tooling

### Development Tools
- Python extensions for VS Code
- Black formatter and Pylint
- TailwindCSS IntelliSense
- Git and GitHub CLI
- Jupyter notebook support

## Getting Started

1. **Open in Dev Container**: Use VS Code's "Reopen in Container" command
2. **Wait for Setup**: The post-create script will automatically:
   - Install Python dependencies
   - Run database migrations
   - Create a superuser (admin/admin123)
   - Set up sample data
   - Configure TailwindCSS

## Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Django App | http://localhost:8000 | - |
| Admin Panel | http://localhost:8000/admin | admin/admin123 |
| Redis | localhost:6379 | - |
| MySQL | localhost:3306 | infikar/infikar123 |

## Environment Variables

Create a `.env` file in the project root with:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://infikar:infikar123@mysql:3306/infikar
REDIS_URL=redis://redis:6379/0
GOOGLE_ANALYTICS_ID=your-ga-id
YOUTUBE_API_KEY=your-youtube-api-key
```

## Development Commands

```bash
# Start Django server
poetry run python manage.py runserver 0.0.0.0:8000

# Run migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Run tests
poetry run python manage.py test

# Collect static files
poetry run python manage.py collectstatic
```

## Troubleshooting

### Redis Connection Issues
If you see Redis connection errors, the app will automatically fall back to local memory cache for development.

### Database Issues
Make sure MySQL is running and accessible. The container will wait for services to be ready before running migrations.

### Port Conflicts
If ports 8000, 6379, or 3306 are already in use, you can modify the port mappings in `docker-compose.yml`.

## Project Structure

```
infikar/
├── .devcontainer/          # Dev container configuration
├── accounts/               # User authentication & profiles
├── cards/                  # Bio site cards & content
├── analytics/              # Analytics & tracking
├── subscriptions/          # Subscription & payment
├── templates/              # Card templates
├── infikar/               # Django project settings
├── static/                # Static files
├── templates/             # HTML templates
└── manage.py              # Django management script
```
