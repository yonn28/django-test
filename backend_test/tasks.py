from celery import shared_task
from backend_test.apps.notifications.models import Notification , Menu, Option, Selection
from django.contrib.auth.models import User
import urllib3
from django.contrib.sites.shortcuts import get_current_site
import json

@shared_task
def send_slack_notifications(id_menu, current_site):
    menu_selected = Menu.objects.get(id=id_menu)
    http = urllib3.PoolManager()
    for person in User.objects.all():
        n1 = Notification(user=person,menu=menu_selected)
        n1.save()
        url_to_send = 'http://%s%s%s' % (current_site.domain, '/menu/', n1.id)
        data = {"text": url_to_send}
        encoded_data = json.dumps(data).encode("utf-8")
        http.request(
            "POST",
            "https://hooks.slack.com/services/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",
            body = encoded_data, 
            headers ={"Content-Type": "application/json"}
        )
        print(url_to_send)