from django.utils import timezone
from .models import WhatsAppMessage
from env.celery_app import app as celery_app
import pywhatkit as kit

@celery_app.task(bind=True, max_retries=1)
def send_whatsapp_message(self, message_id):
    try:
        msg = WhatsAppMessage.objects.get(id=message_id, status='pending')
        kit.sendwhatmsg_instantly( msg.phone_number,msg.message,wait_time=20,tab_close=True,close_time=5)
        msg.status = 'sent'
        msg.sent_at = timezone.now()
        msg.save()
        return f"Message sent to {msg.phone_number}"
    except WhatsAppMessage.DoesNotExist:
        return "Message not found or already processed"
    except Exception as e:
        try:
            msg = WhatsAppMessage.objects.get(id=message_id)
            msg.status = 'failed'
            msg.error_message = str(e)
            msg.save()
        except WhatsAppMessage.DoesNotExist:
            pass
        raise self.retry(exc=e, countdown=60)