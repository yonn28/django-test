from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.



class Option(models.Model):
    id = models.AutoField(primary_key=True )
    description = models.TextField()

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    options = models.ManyToManyField(Option)
    date = models.DateTimeField(auto_now_add= True)


class Notification(models.Model):
    id = models.UUIDField( primary_key=True, default= uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)
    class Meta:
        permissions = [('can_send_notifications', 'Can Send Notifications')]


class Selection(models.Model):
    uuid = models.ForeignKey(Notification, on_delete=models.CASCADE)
    option_selected = models.ForeignKey( Option, null=True, on_delete=models.CASCADE)
    note = models.TextField()
    date = models.DateTimeField(auto_now_add= True)

