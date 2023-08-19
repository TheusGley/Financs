import datetime
from django.conf import settings
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity_iso = datetime.datetime.fromisoformat(last_activity)
                timeout_duration = getattr(settings, 'SESSION_TIMEOUT_DURATION')  # 60 segundos
                time_difference = datetime.datetime.now() - last_activity_iso
                if time_difference.total_seconds() > timeout_duration:
                    request.session.flush()  # Limpar a sessão
                    return redirect('logout') 

            request.session['last_activity'] = datetime.datetime.now().isoformat()

        response = self.get_response(request)
        return response
