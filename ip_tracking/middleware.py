from django.contrib.gis import geoip2
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import datetime
from django.core.cache import cache
import geoip2.database
import os

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Path to GeoLite2-City database
        self.geo_db_path = os.path.join(os.path.dirname(__file__), "GeoLite2-City.mmdb")
        self.reader = geoip2.database.Reader(self.geo_db_path)

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path

        # Block IP check
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Check cache for geolocation
        geo_data = cache.get(f'geo_{ip}')
        if not geo_data:
            try:
                response = self.reader.city(ip)
                geo_data = {
                    "country": response.country.name,
                    "city": response.city.name
                }
            except Exception:
                geo_data = {"country": None, "city": None}

            # Cache for 24 hours
            cache.set(f'geo_{ip}', geo_data, timeout=60*60*24)

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=datetime.datetime.now(),
            country=geo_data.get("country"),
            city=geo_data.get("city")
        )

        response = self.get_response(request)
        return response