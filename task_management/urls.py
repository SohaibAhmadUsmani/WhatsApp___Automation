from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_message, name='schedule_message'),
    path('status/', views.message_status, name='message_status'),
]
