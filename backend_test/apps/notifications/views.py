from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from .models import Notification , Menu, Option, Selection
from django.views import View 
from django.views.generic import CreateView
from django.utils import timezone
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
import urllib3
import json
from backend_test.tasks import send_slack_notifications

PERMISSIONS_REQUIRED = 'notifications.can_send_notifications'

class CreateNotification(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = PERMISSIONS_REQUIRED
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        return render(request,'notifications/create_notification.html',context={'menus':menus})

    def post(self, request, *args, **kwargs):
        '''this is for notify all the users the link for select the meal'''
        menus = Menu.objects.all()
        send_slack_notifications(request.POST.get("response"), get_current_site(request))
        return render(request,'notifications/create_notification.html',context={'menus':menus})


class AddOption(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = PERMISSIONS_REQUIRED
    model = Option
    template_name = 'notifications/add_optionform.html'
    success_url=reverse_lazy('notifications:create')
    fields = ['description']


class AddNewMenu(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = PERMISSIONS_REQUIRED
    def get(self, request, *args, **kwargs):
        options = Option.objects.all()
        return render(request,'notifications/add_menuform.html',context={'options':options})
    def post(self, request, *args, **kwargs):
        options_selected = Option.objects.filter(description__in = list(request.POST)[1:])
        M1 = Menu()
        M1.save()
        for option in options_selected:
            M1.options.add(option.id)
        return HttpResponseRedirect(reverse_lazy('notifications:create'))


class WatchMenu(View):
    def get(self, request, *args, **kwargs):
        ''' this is for get the context for menu display and selection, before the 11AM colombian timezone, you must be logged out for work !!!'''
        pk = self.kwargs.get('pk',0)
        hour_actual = timezone.localtime(timezone.now()).hour
        if hour_actual > 11:
            return render(request,'notifications/not_valid_hour.html',context={})
        name = Notification.objects.filter(id=pk).values_list('user__username',flat=True)[0]
        menus_ids = Notification.objects.filter(id=pk).values_list('menu__options',flat=True)
        menus = Option.objects.filter(id__in=list(menus_ids))
        return render(request,'notifications/choose.html',context={'menus':menus,'username':name, 'pk':pk })
    
    def post(self,request, *args, **kwargs):
        ''' this is for save user selection in de db '''
        pk = self.kwargs.get('pk',0)
        name = Notification.objects.filter(id=pk).values_list('user__username',flat=True)[0]
        option_form = Option.objects.get(id=request.POST.get("response"))
        note_form = request.POST.get("personalization")
        notification_form = Notification.objects.get(id=pk)
        Selection.objects.update_or_create(uuid = notification_form ,option_selected = option_form, note = note_form)
        menus_ids = Notification.objects.filter(id=pk).values_list('menu__options',flat=True)
        menus = Option.objects.filter(id__in=list(menus_ids))
        return render(request,'notifications/choose.html',context={'menus':menus,'username':name, 'pk':pk})