from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.views.decorators.csrf import csrf_exempt
from .models import WhatsAppMessage
from .tasks import send_whatsapp_message

@csrf_exempt
def schedule_message(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        message = request.POST.get('message')
        scheduled = request.POST.get('scheduled_time')
        if phone and message and scheduled:
            msg = WhatsAppMessage.objects.create(
                phone_number=phone,
                message=message,
                scheduled_time=scheduled,
                status='pending'
            )
            send_whatsapp_message.apply_async(
                args=[msg.id],
                eta=msg.scheduled_time
            )
            django_messages.success(request, 'Message scheduled successfully!')
            return redirect('schedule_message')
        else:
            django_messages.error(request, 'All fields are required.')
    return render(request, 'schedule.html')
def message_status(request):
    msgs = WhatsAppMessage.objects.all().order_by('-created_at')
    return render(request, 'status.html', {'messages': msgs})