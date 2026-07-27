# Celery + Redis (reference only — not wired in this project)

**What it is:** Background jobs. API enqueues work → Redis holds queue → worker runs task later.  
**Same as:** BullMQ + Redis in NestJS.  
**Not the same as:** Python `async/await`.

---

## Flow

```
POST /api/run-billing/  →  view calls task.delay(5)
        ↓
   Redis (broker) stores message
        ↓
   celery worker (separate process) picks message
        ↓
   runs @shared_task function  →  Postgres / services.py
```

---

## Install

```bash
pip install celery redis
# Redis must be running locally:
# brew install redis && redis-server
```

Add to `.env`:
```
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## File 1: `config/celery.py`

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')                                    # app name — yours
app.config_from_object('django.conf:settings', namespace='CELERY')  # fixed — reads settings
app.autodiscover_tasks()                                    # fixed — finds tasks.py in INSTALLED_APPS
```

| Code | Meaning |
|------|---------|
| `Celery` | fixed — Celery library class |
| `'config'` | yours — project name |
| `namespace='CELERY'` | fixed — settings keys must start with `CELERY_` |
| `autodiscover_tasks()` | fixed — auto-imports `tasks.py` from each app |

---

## File 2: `config/__init__.py`

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

Loads Celery when Django starts. **Fixed pattern** for Django + Celery.

---

## File 3: `config/settings.py` (add)

```python
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
```

| Setting | Meaning |
|---------|---------|
| `CELERY_BROKER_URL` | fixed setting name — **where jobs are queued** (Redis) |
| `CELERY_RESULT_BACKEND` | fixed — where task results are stored (optional, often same Redis) |
| `redis://localhost:6379/0` | Redis URL — host, port, DB number |

---

## File 4: `billing/tasks.py`

```python
from celery import shared_task
from .services import calculate_customer_total_fast


@shared_task                                                   # fixed decorator
def run_customer_billing(customer_id):                         # yours — task name
    total, _ = calculate_customer_total_fast(customer_id)
    return str(total)
```

| Code | Meaning |
|------|---------|
| `@shared_task` | fixed — marks function as Celery task (works in any Django app) |
| `run_customer_billing` | yours — function name becomes task name |
| `return str(total)` | optional result stored in Redis if result backend set |

---

## File 5: call from view (example)

```python
from billing.tasks import run_customer_billing

@action(detail=False, methods=['post'], url_path='run-billing')
def run_billing(self, request):
    customer_id = request.data.get('customer_id')
    run_customer_billing.delay(customer_id)    # fixed — enqueue, returns immediately
    return Response({'status': 'queued', 'customer_id': customer_id}, status=202)
```

| Code | Meaning |
|------|---------|
| `.delay(customer_id)` | fixed — send job to Redis, **does not wait** for result |
| `status=202` | HTTP "accepted" — job started, not finished |

**Without Celery:** you'd call `calculate_customer_total_fast()` here and user waits.

---

## Run worker (separate terminal)

```bash
celery -A config worker -l info
```

| Part | Meaning |
|------|---------|
| `celery` | fixed CLI |
| `-A config` | yours — Django project module (where `celery.py` lives) |
| `worker` | fixed — start consumer process |
| `-l info` | log level |

**3 processes needed:** `runserver` + `redis-server` + `celery worker`

---

## BullMQ map

| Celery | BullMQ |
|--------|--------|
| Redis broker | Redis connection |
| `@shared_task` | job handler / processor |
| `.delay()` | `queue.add()` |
| `celery worker` | BullMQ worker |
| `billing/tasks.py` | `billing.processor.ts` |

---

## Interview one-liner

> "Sync DRF views enqueue long billing work via Celery `.delay()` to Redis. Workers run service-layer logic in a separate process — same as BullMQ."
