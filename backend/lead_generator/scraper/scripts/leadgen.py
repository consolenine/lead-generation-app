import os
import django
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

import asyncio
import pandas as pd
from scraper.requester.queues import UserQueue
from scraper.requester.request_queue import RequestQueue
from django.db import transaction
from asgiref.sync import sync_to_async
from scraper.models import ScrapingTask, Lead
from django.contrib.auth.models import User
from channels.layers import get_channel_layer

MAX_RUNNING_TASKS = 2

async def fetch_tasks_from_database():
    running_tasks_count = await sync_to_async(
        ScrapingTask.objects.filter(status=ScrapingTask.StatusChoices.IN_PROGRESS).count
    )()
    
    if running_tasks_count < MAX_RUNNING_TASKS:
        tasks_to_start = MAX_RUNNING_TASKS - running_tasks_count
        
        queued_tasks = await sync_to_async(
            lambda: list(ScrapingTask.objects.filter(status=ScrapingTask.StatusChoices.QUEUED).order_by('created_at')[:tasks_to_start])
        )()
        return queued_tasks
    return []

async def leadGenerator(owner, task_id, users=[], filters=None, updates_channel=None):
    print(f"Processing task: {task_id}, Owner: {owner}")
    playlist_debug = []
    playlist_debug_headers = ["Playlist URL", "Playlist Title", "Playlist Description"]
    main_queue = RequestQueue(
        owner, task_id, users=users, limit=100, filters=filters, playlist_debug=playlist_debug, updates_channel=updates_channel
    )

    leads = await main_queue.run()

    df = pd.DataFrame(playlist_debug, columns=playlist_debug_headers)
    df.to_csv(f"playlist_debug_{task_id}.csv", index=False, encoding="utf-8")

    print(f"Task {task_id} completed.")
    return leads

def update_task_status_to_in_progress(task):
    with transaction.atomic():
        task.status = ScrapingTask.StatusChoices.IN_PROGRESS
        task.save()

def update_task_status_to_completed(task):
    with transaction.atomic():
        task.status = ScrapingTask.StatusChoices.COMPLETED
        task.save()

def update_task_status_to_failed(task):
    with transaction.atomic():
        task.status = ScrapingTask.StatusChoices.FAILED
        task.save()

def update_leads_to_db(data, task):
    with transaction.atomic():
        owner = User.objects.get(id=task.owner_id)
        
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
                    owner=owner,
                    parent_task=task,
                )
                for item in data
            ]
        )

async def process_tasks():
    while True:
        tasks = await fetch_tasks_from_database()
        
        if not tasks:
            print("Waiting For Tasks...")
            await asyncio.sleep(10)
            continue
        
        for task in tasks:
            channel_layer = get_channel_layer()
            users, filters = task.config["users"], task.config
            
            # Update the task status to IN_PROGRESS atomically
            await sync_to_async(update_task_status_to_in_progress)(task)
            
            results = []
            try:
                results = await leadGenerator(
                    owner=task.owner_id, 
                    task_id=task.id, 
                    users=users, 
                    filters=filters, 
                    updates_channel=channel_layer
                )
            except Exception as e:
                await sync_to_async(update_task_status_to_failed)(task)
                print(e)
                continue
            finally:
                data = []
                for item in results:
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
                
                # Update the leads to the database atomically
                await sync_to_async(update_leads_to_db)(data, task)
                await sync_to_async(update_task_status_to_completed)(task)
        
        await asyncio.sleep(10)

def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process_tasks())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()