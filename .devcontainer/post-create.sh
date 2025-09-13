#!/bin/bash

# Post-create script for Infikar development container

echo "🚀 Setting up Infikar development environment..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
poetry install

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "🗄️ Running database migrations..."
poetry run python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
poetry run python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Create some sample data
echo "📊 Creating sample data..."
poetry run python manage.py shell -c "
from cards.models import CardTemplate
from accounts.models import User

# Create default templates
templates = [
    {'name': 'Minimal', 'slug': 'minimal', 'description': 'Clean and minimal design'},
    {'name': 'Modern', 'slug': 'modern', 'description': 'Modern and sleek design'},
    {'name': 'Creative', 'slug': 'creative', 'description': 'Creative and artistic design'},
    {'name': 'Professional', 'slug': 'professional', 'description': 'Professional business design'},
    {'name': 'Colorful', 'slug': 'colorful', 'description': 'Bright and colorful design'},
]

for template_data in templates:
    template, created = CardTemplate.objects.get_or_create(
        slug=template_data['slug'],
        defaults=template_data
    )
    if created:
        print(f'Created template: {template.name}')
    else:
        print(f'Template already exists: {template.name}')
"

# Collect static files
echo "📁 Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Create .env file if it doesn't exist
echo "⚙️ Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
DATABASE_URL=mysql://infikar:infikar123@mysql:3306/infikar
REDIS_URL=redis://redis:6379/0
GOOGLE_ANALYTICS_ID=
YOUTUBE_API_KEY=
APPLE_CLIENT_ID=
APPLE_SECRET=
APPLE_KEY=
EOF
    echo "Created .env file"
else
    echo ".env file already exists"
fi

# Set up TailwindCSS
echo "🎨 Setting up TailwindCSS..."
if [ ! -f tailwind.config.js ]; then
    npx tailwindcss init
    echo "Created TailwindCSS config"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🔗 Available services:"
echo "   - Django: http://localhost:8000"
echo "   - Admin: http://localhost:8000/admin (admin/admin123)"
echo "   - Redis: localhost:6379"
echo "   - MySQL: localhost:3306"
echo ""
echo "🚀 To start the development server:"
echo "   poetry run python manage.py runserver 0.0.0.0:8000"
echo ""
echo "📚 Happy coding! 🎉"
