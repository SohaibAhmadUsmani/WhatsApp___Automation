from django.contrib import admin
from .models import WhatsAppMessage

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'message', 'scheduled_time', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'scheduled_time']
    search_fields = ['phone_number', 'message']
    readonly_fields = ['status', 'sent_at', 'error_message', 'created_at']
