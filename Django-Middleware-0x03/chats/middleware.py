# chats/middleware.py

import time
from collections import defaultdict
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow only between 18:00 (6PM) and 21:00 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)  # {ip_address: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/chats/'):
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.message_log[ip] = [
                timestamp for timestamp in self.message_log[ip]
                if current_time - timestamp < 60
            ]

            # Check if user has exceeded the message limit
            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again in a minute.")

            self.message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Allow unauthenticated requests to proceed
        if not user.is_authenticated:
            return self.get_response(request)

        # Only allow users with 'admin' or 'moderator' roles
        if hasattr(user, 'role') and user.role not in ['admin', 'moderator']:
            return JsonResponse({'error': 'Permission denied: insufficient role'}, status=403)

        return self.get_response(request)
