from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from . import models
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1️⃣ IPs with >100 requests in last hour
    request_counts = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('id'))
    )

    for entry in request_counts:
        if entry['count'] > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=entry['ip_address'],
                reason=f"More than 100 requests in the last hour"
            )

    # 2️⃣ IPs accessing sensitive paths
    sensitive_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS)
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}"
        )
