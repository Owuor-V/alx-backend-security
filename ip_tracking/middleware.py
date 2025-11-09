from .models import RequestLog
import datetime

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path

        # Log request in DB
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=datetime.datetime.now()
        )

        response = self.get_response(request)
        return response
