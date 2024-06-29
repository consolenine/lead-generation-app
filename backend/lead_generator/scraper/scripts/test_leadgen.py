import os
import django
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lead_generator.settings')
django.setup()

import asyncio, pandas as pd
from scraper.requester.request_queue import RequestQueue

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

async def process_tasks():
    task = {
        "owner_id": 1,
        "id": 1,
        "config": {
            "users": ["terence12345"],
            "filters": {
                "tags": ["deep ambient", "oneheart", "dark and ambient", "aesthetic", "dark", "ambient", "relaxing ambient"],
                "all_tags": False,
                "last_updated": "2023-01-01",
                "min_likes": 100,
                "max_likes": 1000000,
                "run_limit": 30,
            }
        }
    }

    users, filters = task["config"]["users"], task["config"]["filters"]
    
    results = []
    try:
        results = await leadGenerator(
            owner=task["owner_id"], 
            task_id=task["id"], 
            users=users, 
            filters=filters
        )
    except Exception as e:
        print(e)

def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process_tasks())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    run()