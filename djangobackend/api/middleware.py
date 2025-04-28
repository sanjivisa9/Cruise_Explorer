from django.http import HttpResponseForbidden
import re

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for SQL injection attempts
        if self._contains_sql_injection(request):
            return HttpResponseForbidden("Potential SQL injection detected")

        # Check for XSS attempts
        if self._contains_xss(request):
            return HttpResponseForbidden("Potential XSS attempt detected")

        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Content-Security-Policy'] = "default-src 'self'"
        
        return response

    def _contains_sql_injection(self, request):
        sql_patterns = [
            r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|INTO|ALTER)\s',
            r'--[^\n]*$',
            r';[^\n]*$'
        ]
        return any(
            re.search(pattern, str(value), re.IGNORECASE)
            for pattern in sql_patterns
            for value in request.GET.values()
        )

    def _contains_xss(self, request):
        xss_patterns = [
            r'<script.*?>',
            r'javascript:',
            r'on\w+\s*=',
            r'data:text/html'
        ]
        return any(
            re.search(pattern, str(value), re.IGNORECASE)
            for pattern in xss_patterns
            for value in request.GET.values()
        )