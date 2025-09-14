"""
Health check endpoint for Docker containers
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis


def health_check(request):
    """
    Health check endpoint that verifies:
    - Database connectivity
    - Redis connectivity
    - Basic application health
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['redis'] = 'healthy'
        else:
            health_status['checks']['redis'] = 'unhealthy'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['checks']['redis'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Return appropriate status code
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JsonResponse(health_status, status=status_code)
