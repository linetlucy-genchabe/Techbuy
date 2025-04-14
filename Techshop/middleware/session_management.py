from django.contrib import auth
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity and (timezone.now().timestamp() - last_activity > settings.SESSION_COOKIE_AGE):
                logout(request)
                request.session.flush()
            else:
                request.session['last_activity'] = timezone.now().timestamp()
        
        response = self.get_response(request)
        return response