from .spotify_auth import getToken, getSeleniumToken
from .queues import *
from .queries import *
from .artist_queries import *
import aiohttp
import asyncio
import traceback
import time
import json
from aiohttp.client_exceptions import ServerDisconnectedError
from asgiref.sync import async_to_sync


class RequestQueue:
    def __init__(self, owner, task_id, users=[], limit=50, filters=None, playlist_debug=None, updates_channel=None):
        self.owner = owner
        self.task_id = task_id
        self.queue = []
        self.size = 0
        self.limit = limit
        self.filters = filters
        self.updates_channel = updates_channel

        self.users = UserQueue()
        self.users.addBack([SpotifyUser(user) for user in users])

        self.dependency_queues = {
            "artist_playlists": ArtistPlaylistQueue(),
            "albums": AlbumQueue(),
            "followers": FollowerQueue(),
            "playlists": PlaylistQueue(),
            "playlist_details": PlaylistDetailedQueue(),
        }
        self.data_queues = {
            "users": self.users,
            "artists": ArtistQueue(),
            "results": ResponseQueue(),
            "playlist_debug": playlist_debug,
        }

        self.__headers = getToken("https://open.spotify.com")
        if self.__headers is None:
            raise Exception("Failed to get token")

        d = getSeleniumToken(
            "https://open.spotify.com/artist/3b2q69EvD3tLQDKiYSd5uo/discovered-on"
        )
        self.__auth_headers = {
            "Content-Type": "application/json",
            "Authorization": d[0],
        }
        self.__persisted_hash = d[1]
        if d[0] is None:
            raise Exception("Failed to get authenticated token. Admin action required.")

    def add_request(self, request):
        self.queue.append(request)
        self.size += 1

    async def refresh_headers(self):
        self.__headers = getToken("https://open.spotify.com")
        if self.__headers is None:
            raise Exception("Failed to get token")

        d = getSeleniumToken(
            "https://open.spotify.com/artist/3b2q69EvD3tLQDKiYSd5uo/discovered-on"
        )
        self.__auth_headers = {
            "Content-Type": "application/json",
            "Authorization": d[0],
        }
        self.__persisted_hash = d[1]
        if d[0] is None:
            raise Exception("Failed to get authenticated token. Admin action required.")

    def is_full(self):
        return self.size >= self.limit

    def is_empty(self):
        return self.size == 0

    def print_status(self):
        print("--------------------")
        print("Leads Generated Till Now: ", self.data_queues["results"].get_size())
        print("Requests In Queue: ", self.size)
        print("Artists In Queue: ", self.data_queues["artists"].get_size())
        print(
            "Artist Playlists Queries In Queue: ",
            self.dependency_queues["artist_playlists"].get_size(),
        )
        print("Artist Albums In Queue: ", self.dependency_queues["albums"].get_size())
        print("Spotify Users In Queue: ", self.data_queues["users"].get_size())
        print(
            "Follower Queries In Queue: ",
            self.dependency_queues["followers"].get_size(),
        )
        print(
            "Playlist Queries In Queue: ",
            self.dependency_queues["playlists"].get_size(),
        )
        print(
            "Playlist Detailed Queries In Queue: ",
            self.dependency_queues["playlist_details"].get_size(),
        )

    async def process_items(self):
        print("Round Started")
        # print("MID-PROCESS")
        # self.print_status()
        if self.is_empty():
            return None
        async with aiohttp.ClientSession() as session:
            try:
                tasks = []
                for r in self.queue:
                    if isinstance(r, PersistedQuery):
                        tasks.append(
                            r.process(
                                session,
                                self.__auth_headers,
                                self.__persisted_hash,
                                self.dependency_queues,
                                self.data_queues,
                                self.filters,
                            )
                        )
                    else:
                        tasks.append(
                            r.process(
                                session,
                                self.__headers,
                                self.dependency_queues,
                                self.data_queues,
                                self.filters,
                            )
                        )

                await asyncio.gather(*tasks)

                # Remove completed requests from queue
                self.queue = list(filter(lambda x: x.processed == 0, self.queue))
                self.size = len(self.queue)

                # with open("leads.json", "w") as f:
                #     data = []
                #     for item in self.data_queues["results"].get_stack():
                #         data.append(
                #             {
                #                 "user": item["user"],
                #                 "links": {
                #                     "free": list(item["links"]["free"]),
                #                     "paid": list(item["links"]["paid"]),
                #                     "others": list(item["links"]["others"]),
                #                 },
                #                 "email": list(item["email"]),
                #                 "phone": list(item["phone"]),
                #                 "related_playlists": list(item["related_playlists"]),
                #             }
                #         )
                #     json.dump(data, f, indent=4)
            except QueueOverflowException as e:
                print(e)
                return

    async def run(self):
        time_started = time.time()
        while True:
            # print("---------START---------")
            # self.print_status()
            # await self.updates_channel.group_send(
            #     f"user_{self.owner}",
            #     {
            #         "type": "send_progress",
            #         "message": {
            #             "task_id": self.task_id,
            #             "progress": self.data_queues["results"].get_size(),
            #             "status": "In Progress",
            #         }
            #     }
            # )
            try:
                stop_conditions = self.size == 0 and all(
                    [queue.is_empty() for queue in self.dependency_queues.values()]
                )

                # Stop collecting leads
                # if self.data_queues["results"].is_full():
                #     return self.data_queues["results"].get_stack()

                # When all other queues are empty except user queue, get new users
                if stop_conditions and not self.data_queues["users"].is_empty():
                    added_count = 0
                    fallback_count = 0
                    temp_users = UserQueue()
                    while not self.data_queues["users"].is_empty() and added_count < 10:
                        if self.dependency_queues["followers"].get_timeout_stat(
                            time=time.time(), timeout=30
                        ):
                            user = self.data_queues["users"].removeFront()
                            try:
                                if not user.playlist_r:
                                    self.dependency_queues["playlists"].addBack(
                                        UserPlaylistQuery(user.uid)
                                    )
                                user.playlist_r = True

                                if user.followers_level < 1:
                                    self.dependency_queues["followers"].addBack(
                                        UserFollowerQuery(
                                            user.uid, user.followers_level
                                        )
                                    )
                                    added_count += 1
                                    self.data_queues["users"].add_exhausted(user.uid)
                                else:
                                    self.data_queues["users"].add_exhausted(user.uid)
                            except QueueOverflowException as e:
                                print(e)
                                break
                            except Exception as e:
                                print(e)
                                break
                        else:
                            user = self.data_queues["users"].removeFront()
                            if not user.playlist_r:
                                self.dependency_queues["playlists"].addBack(
                                    UserPlaylistQuery(user.uid)
                                )
                                fallback_count += 1
                            user.playlist_r = True
                            temp_users.addBack(user)
                        
                    if added_count != 0:
                        self.dependency_queues["followers"].last_updated = time.time()
                    while not temp_users.is_empty():
                        self.data_queues["users"].addBack(temp_users.removeFront())

                # Adding Artists Playlist Queries
                stop_conditions = self.size == 0 and all(
                    [queue.is_empty() for queue in self.dependency_queues.values()]
                )

                if stop_conditions and self.data_queues["users"].is_empty():
                    if self.data_queues["artists"].is_empty():
                        return self.data_queues["results"].get_stack()

                    added_count = 0
                    while (
                        not self.data_queues["artists"].is_empty() and added_count < 100
                    ):
                        artist = self.data_queues["artists"].removeFront()
                        try:
                            self.dependency_queues["artist_playlists"].addBack(
                                ArtistDiscoveredOnQuery(artist)
                            )
                            self.dependency_queues["artist_playlists"].addBack(
                                ArtistFeaturingQuery(artist)
                            )
                            self.dependency_queues["artist_playlists"].addBack(
                                ArtistRelatedQuery(artist)
                            )
                            self.dependency_queues["artist_playlists"].addBack(
                                ArtistAppearsOnQuery(artist)
                            )
                            added_count += 4
                            self.data_queues["artists"].add_exhausted(artist)
                        except QueueOverflowException as e:
                            print(e)
                            break
                        except Exception as e:
                            print(e)
                            break
                    if added_count != 0:
                        self.dependency_queues["artist_playlists"].last_updated = (
                            time.time()
                        )
                
                # print("---------BEFORE PROCESSING---------")
                # self.print_status()

                # Fill up the queue with items from the associated queues

                for queue in reversed(self.dependency_queues.values()):

                    if self.is_full():
                        break

                    while not queue.is_empty():
                        if self.is_full():
                            break

                        item = queue.removeFront()

                        self.add_request(item)
                
                

                # Process the items in the queue
                await self.process_items()

                print("---------STATUS---------")
                print("TIME RUNNING (seconds): ", int(time.time() - time_started))
                print("TIME RUNNING (minutes): ", (time.time() - time_started) // 60)
                self.print_status()
                if (time.time() - time_started) // 60 >= int(self.filters["run_limit"]):
                    print("Process Timeout....Exiting")
                    break
            except QueryFailedException as e:
                if e.meta.get("status") == 401:
                    await self.refresh_headers()
                    continue
                print("Warning....API Overflow....Sleeping until timeout")
                traceback.print_exc()
                time.sleep(10)
                continue
            except ServerDisconnectedError as e:
                print("API disconnected....Reconnecting")
                time.sleep(10)
                await self.refresh_headers()
                continue
            except Exception as e:
                print(e)
                print("UNCAUGHT")
                traceback.print_exc()
                break

        return self.data_queues["results"].get_stack()
