import asyncio
import pandas as pd
from .requester.queues import UserQueue
from .requester.request_queue import RequestQueue


async def leadGenerator(owner, task_id, users=[], filters=None, updates_channel=None):
    print(filters)
    playlist_debug = []
    playlist_debug_headers = ["Playlist URL", "Playlist Title", "Playlist Description"]
    main_queue = RequestQueue(
        owner, task_id, users=users, limit=100, filters=filters, playlist_debug=playlist_debug, updates_channel=updates_channel
    )

    leads = await main_queue.run()

    df = pd.DataFrame(playlist_debug, columns=playlist_debug_headers)
    df.to_csv("playlist_debug.csv", index=False, encoding="utf-8")

    return leads


if __name__ == "__main__":
    # asyncio.run(leadGenerator("rfy3991wwpjvgh3k1825inhnm"))
    asyncio.run(
        leadGenerator(
            users=[
                "ferranalemanyroig",
                "31i2md4tnp7lowsqsqbjxlm56emq",
                "31hdx443wpbgnbrioaetwnyffp3y",
                "1qnjw6kks0gxfzrpjdvgth5p6",
                "6k5wm1aav3cxdrwwrox0n3fqu",
            ],
            filters={
                "min_likes": 1000,
                "last_updated": "2015-01-01",
                "tags": ["rock"],
                "lead_type": ["email", "links", "phone"],
                "max_leads": 20,
            },
        )
    )
