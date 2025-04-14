import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryTrackerPhase1.settings')

app = Celery('InventoryTrackerPhase1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()