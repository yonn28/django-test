from django.urls import path
from .views import CreateNotification, WatchMenu, AddOption,AddNewMenu

app_name = 'notifications'

urlpatterns = [
    path('', CreateNotification.as_view(), name='create'),
    path('option', AddOption.as_view(), name='create_option'),
    path('menu', AddNewMenu.as_view(), name='create_menu'),
    path('menu/<uuid:pk>', WatchMenu.as_view(), name='see_menu' )
]
