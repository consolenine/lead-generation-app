from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.db import transaction
from .models import ScrapingTask, Lead
from .leadgen  import leadGenerator
import asyncio

MAX_RUNNING_TASKS = 2

@shared_task
def check_queued_tasks():
    running_tasks_count = ScrapingTask.objects.filter(status=ScrapingTask.StatusChoices.IN_PROGRESS).count()
    
    if running_tasks_count < MAX_RUNNING_TASKS:
        tasks_to_start = MAX_RUNNING_TASKS - running_tasks_count
        
        queued_tasks = ScrapingTask.objects.filter(status=ScrapingTask.StatusChoices.QUEUED).order_by('created_at')[:tasks_to_start]
        
        for task in queued_tasks:
            # Update the task status to avoid race conditions
            with transaction.atomic():
                task.status = ScrapingTask.StatusChoices.IN_PROGRESS
                task.save()
                scrape_leads.delay(task.id)


@shared_task
def scrape_leads(task_id):
    task = ScrapingTask.objects.get(id=task_id)
    
    channel_layer = get_channel_layer()
    
    users, filters = task.config["users"], task.config["filters"]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(leadGenerator(
            owner=task.owner_id,
            task_id=task.id,
            users=users,
            filters=filters,
            updates_channel=channel_layer
        ))
        if result:
            task.status = "Completed"
            task.save()
    except asyncio.CancelledError as e:
        task.status = "Failed"
        task.save()
        print(e)
    except Exception as e:
        task.status = "Failed"
        task.save()
        print(e)

    data = []
    for item in result:
        data.append(
            {
                "user": item["user"],
                "links": {
                    "free": list(item["links"]["free"]),
                    "paid": list(item["links"]["paid"]),
                    "others": list(item["links"]["others"]),
                },
                "email": list(item["email"]),
                "phone": list(item["phone"]),
                "related_playlists": list(item["related_playlists"]),
            }
        )
    
    Lead.objects.bulk_create(
        [
            Lead(
                spotify_username=item["user"] or "Placeholder",
                email=item["email"],
                phone=item["phone"],
                related_playlists=item["related_playlists"],
                free_links=item["links"]["free"],
                paid_links=item["links"]["paid"],
                others_links=item["links"]["others"],
                owner=task.owner_id,
                parent_task=task,
            )
            for item in data
        ]
    )

    return JsonResponse(data, safe=False)