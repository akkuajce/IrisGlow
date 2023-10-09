# middleware.py
from django.middleware.cache import CacheMiddleware

class NoCacheMiddleware(CacheMiddleware):
    def process_response(self, request, response):
        # Add Cache-Control and Expires headers to prevent caching
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Expires'] = '0'
        return response
