# WhatsApp Message Scheduler

Automate WhatsApp message delivery using Celery (task queue) + Redis (message broker). Schedule messages to be sent at a specific time via WhatsApp Web, without blocking your WhatsApp account.

## How It Works

1. User schedules a message via the Django web form
2. Message is saved to the database with `status=pending`
3. Celery `apply_async(eta=...)` stores the task in Redis with the exact delivery time
4. When the time arrives, the Celery Worker picks up the task
5. PyWhatKit opens Chrome → WhatsApp Web → sends the message
6. Database status updates to `sent` or `failed`

No infinite loops. No polling. Each message is a one-shot scheduled task.

## Tech Stack

- **Backend:** Django 6.0
- **Task Queue:** Celery 5.6
- **Message Broker:** Redis (Redis Cloud)
- **WhatsApp Automation:** PyWhatKit (Chrome WebDriver)
- **Database:** SQLite (default, swappable)

## Project Structure

```
WAAutomation/
├── env/
│   ├── __init__.py          # Celery app import
│   ├── celery_app.py        # Celery app configuration
│   ├── settings.py           # Django settings + Celery config
│   ├── urls.py               # Root URL routing
│   └── ...
├── task_management/
│   ├── models.py             # WhatsAppMessage model
│   ├── tasks.py              # Celery task (send message)
│   ├── views.py              # Schedule form + status page
│   ├── admin.py              # Admin panel registration
│   ├── urls.py               # App URL routing
│   └── templates/
│       ├── schedule.html     # Message scheduling form
│       └── status.html       # Message delivery status table
├── manage.py
└── requirements.txt
```

## Setup Guide

### Prerequisites

- Python 3.10+
- Chrome browser (for WhatsApp Web)
- Redis (cloud or local) — get free at https://redis.com/try-free

### 1. Clone & Install

```bash
git clone <repo-url>
cd WAAutomation
python -m venv env
env\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Configure Redis

In `env/settings.py`, replace the broker URL with your Redis connection string:

```python
CELERY_BROKER_URL = 'redis://default:YOUR_PASSWORD@YOUR_HOST:YOUR_PORT'
CELERY_RESULT_BACKEND = 'redis://default:YOUR_PASSWORD@YOUR_HOST:YOUR_PORT'
```

### 3. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser   # Optional, for admin panel
```

### 4. Start the Application (3 Terminals)

**Terminal 1 — Celery Worker:**
```bash
celery -A env worker --loglevel=info --pool=solo
```

**Terminal 2 — Django Server:**
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/whatsapp/schedule/` to schedule messages.

## Safety Features

- **No infinite loops** — each message is scheduled once via Celery ETA
- **No retry spam** — maximum 1 retry, then marked `failed`
- **Status tracking** — each message has `pending → sent/failed` lifecycle
- **No polling** — Celery ETA delivers the task at the exact scheduled time

## Important Notes

- WhatsApp Web must be logged in for messages to send
- PyWhatKit temporarily takes over keyboard/mouse for ~3 seconds while sending
- Use country code format: `+923001234567`
- Free Redis Cloud tier is sufficient for personal/small-scale use

## License

MIT
