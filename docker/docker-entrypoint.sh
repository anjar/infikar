#!/bin/bash
set -e

# Exit codes
EXIT_CODE=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Wait for database to be ready
wait_for_db() {
    log_info "Waiting for database to be ready..."
    while ! python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infikar.settings')
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    exit(0)
except Exception:
    exit(1)
" >/dev/null 2>&1; do
        log_warn "Database is unavailable - sleeping"
        sleep 1
    done
    log_info "Database is ready!"
}

# Wait for Redis to be ready
wait_for_redis() {
    log_info "Waiting for Redis to be ready..."
    while ! python -c "import redis; r = redis.Redis(host='redis', port=6379, db=0); r.ping()" >/dev/null 2>&1; do
        log_warn "Redis is unavailable - sleeping"
        sleep 1
    done
    log_info "Redis is ready!"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    python manage.py migrate --noinput
}

# Collect static files
collect_static() {
    log_info "Collecting static files..."
    python manage.py collectstatic --noinput
}

# Create superuser if it doesn't exist
create_superuser() {
    log_info "Creating superuser if needed..."
    python manage.py shell -c "
from infikar.accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
" || log_warn "Failed to create superuser"
}

# Main execution
main() {
    log_info "Starting Infikar application..."
    
    # Wait for dependencies
    wait_for_db
    wait_for_redis
    
    # Run setup tasks
    run_migrations
    collect_static
    create_superuser
    
    log_info "Setup complete! Starting application..."
    
    # Execute the main command
    exec "$@"
}

# Run main function with all arguments
main "$@"
