# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Only allow access between 6PM (18) and 9PM (21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(list)  # IP -> list of timestamps

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up old timestamps (older than 60 seconds)
            self.message_logs[ip] = [t for t in self.message_logs[ip] if now - t < 60]

            if len(self.message_logs[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Only 5 messages allowed per minute.")

            # Log current message timestamp
            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict POST requests (e.g., sending messages)
        if request.method == 'POST':
            user = request.user
            # Check if user is authenticated and has role attribute
            if not user.is_authenticated or not hasattr(user, 'role'):
                return HttpResponseForbidden("Access denied. User role not defined.")

            if user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied. Insufficient permissions.")

        return self.get_response(request)
