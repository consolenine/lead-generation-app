from .exceptions import QueryFailedException
from .filter import extract_contacts, validate_contact
from math import ceil
from datetime import datetime
import csv


class BaseQuery:
    def __init__(self, url):
        self.url = url
        self.processed = 0

    async def getAsync(self, session, headers):
        """
        Process a GET request asynchronously.
        """
        response = None
        try:
            async with session.get(self.url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return response.status
        except Exception as e:
            print(e)
            print(self.url)
            print(headers)


class AuthenticatedQuery:
    def __init(self):
        pass


class PersistedQuery:
    def __init(self):
        pass


class SpotifyUser:
    def __init__(self, user, followers_level=0):
        self.uid = user
        self.followers_level = followers_level
        self.playlist_r = False


class UserFollowerQuery(BaseQuery):
    def __init__(self, user, followers_level):
        self.user = user
        self.followers_level = followers_level
        super().__init__(
            f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{self.user}/followers?market=from_token"
        )

    async def process(
        self, session, headers, callback_queues, data_queues, filters=None
    ):
        """
        Async function to get followers of a user.
        Adds Followers to UserStack afterwards.
        """

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"User {self.user} not found")
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to get followers: {response}", {"status": response}
                )
            self.processed += 1
            return

        if response.get("profiles") is not None:
            for profile in response["profiles"]:
                uid = profile["uri"].split(":")[-1]
                
                if not data_queues["users"].has(uid):
                    data_queues["users"].addBack(
                        SpotifyUser(uid, followers_level=self.followers_level + 1)
                    )

        self.processed += 1

class SearchPlaylistQuery(BaseQuery):
    def __init__(self, keywords, offset=0):
        self.keywords = keywords
        self.query = "+".join(keywords)
        self.offset = offset
        super().__init__(
            f"https://api.spotify.com/v1/search?q={self.query}&type=playlist&limit=50&offset={self.offset}"
        )

    async def process(
        self, session, headers, callback_queues, data_queues, filters=None
    ):
        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Unable to process")
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to search playlists: {response}", {"status": response}
                )
            self.processed += 1
            return

        if response.get("playlists") is not None:
            for playlist in response["playlists"]["items"]:
                if not callback_queues["playlists"].has(playlist["owner"]["id"]):
                    playlist_query = UserPlaylistQuery(playlist["owner"]["id"], playlist["owner"]["display_name"], 0)
                    callback_queues["playlists"].addBack(playlist_query)

                    data_queues["users"].addBack(playlist["owner"]["id"])

            if response["playlists"]["total"] > 50 and self.offset == 0:
                max_next = response["playlists"]["total"] // 50
                for i in range(1, max_next):
                    playlist_query = SearchPlaylistQuery(self.keywords, i * 50)
                    callback_queues["searches"].addBack(playlist_query)

        self.processed += 1


class UserPlaylistQuery(BaseQuery):
    def __init__(self, user, username="", offset=0):
        self.user = user
        self.username = username
        self.offset = offset
        super().__init__(
            f"https://api.spotify.com/v1/users/{self.user}/playlists?limit=100&offset={self.offset}"
        )

    async def process(
        self, session, headers, callback_queues, data_queues, filters=None
    ):
        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Playlists for {self.user} not found")
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to get playlists: {response}", {"status": response}
                )
            self.processed += 1
            return

        if response.get("items") is not None:
            dead = True
            for item in response["items"]:
                data_queues["playlist_debug"].append(
                    [
                        item["external_urls"]["spotify"],
                        item["name"],
                        item["description"],
                    ]
                )

                # Queue Detailed Playlist Info Query If keyword matches
                description = item["description"]
                title = item["name"]

                if len(filters.get("tags")) > 0:

                    words_in_string = description.lower()
                    if filters.get("search_title"):
                        words_in_string += " " + title.lower()

                    if filters.get("all_tags") and all(
                        word.lower() in words_in_string for word in filters.get("tags")
                    ):
                        playlist_query = PlaylistDetailsQuery(
                            item["owner"]["id"], item["owner"]["display_name"], item["id"]
                        )
                        callback_queues["playlist_details"].addBack(playlist_query)

                        if not data_queues["users"].has(item["owner"]["id"]):
                            data_queues["users"].addBack(
                                SpotifyUser(item["owner"]["id"], followers_level=1)
                            )

                    elif any(
                        word.lower() in words_in_string for word in filters.get("tags")
                    ):
                        playlist_query = PlaylistDetailsQuery(
                            item["owner"]["id"], item["owner"]["display_name"], item["id"]
                        )
                        callback_queues["playlist_details"].addBack(playlist_query)

                        if not data_queues["users"].has(item["owner"]["id"]):
                            data_queues["users"].addBack(
                                SpotifyUser(item["owner"]["id"], followers_level=1)
                            )

                else:
                    playlist_query = PlaylistDetailsQuery(self.user, item["id"])
                    callback_queues["playlists"].addBack(playlist_query)

            # user = user_queue.get_user(self.user)
            # if user is not None:
            #     user.dead = dead

        # if response.get("total") > 100:
        #     max_next = min(ceil(response["total"]//100), 10)
        #     for offset in range(1, max_next):
        #         playlist_query = UserPlaylistQuery(self.user, offset)
        #         callback_queues[1].addBack(playlist_query)

        self.processed += 1


class UserFromPlaylistQuery(BaseQuery):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        super().__init__(
            f"https://api.spotify.com/v1/playlists/{self.playlist_id}?fields=owner"
        )

    async def process(
        self, session, headers, callback_queues, data_queues, filters=None
    ):
        response = await self.getAsync(session, headers)

        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Playlist data for  {self.playlist_id} not found")
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to get playlist: {response}", {"status": response}
                )

            self.processed += 1
            return

        if response.get("owner") is not None:
            if not data_queues["users"].has(response["owner"]["id"]):
                data_queues["users"].addBack(
                    SpotifyUser(user=response["owner"]["id"], followers_level=1)
                )
        self.processed += 1


class PlaylistDetailsQuery(BaseQuery):
    def __init__(self, user, username, id):
        self.user = user
        self.username = username
        self.playlist_id = id
        super().__init__(f"https://api.spotify.com/v1/playlists/{self.playlist_id}")

    async def process(
        self, session, headers, callback_queues, data_queues, filters=None
    ):
        response = await self.getAsync(session, headers)

        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Playlist data for  {self.playlist_id} not found")
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to get playlist: {response}", {"status": response}
                )

            self.processed += 1
            return

        if response.get("followers")["total"] is not None:

            if response.get("followers")["total"] > filters.get(
                "min_likes"
            ) and response.get("followers")["total"] < filters.get("max_likes"):
                # Add Unique Artists
                try:
                    tracks = response["tracks"]["items"]
                    for track in tracks:
                        if (
                            track["track"] is not None
                            and track["track"]["artists"] is not None
                        ):
                            for artist in track["track"]["artists"]:
                                if not data_queues["artists"].has(artist["id"]):
                                    data_queues["artists"].addBack(artist["id"])
                except Exception as e:
                    pass

                total_tracks = response["tracks"]["total"]
                last_updated = datetime.strptime(filters["last_updated"], "%Y-%m-%d")

                if total_tracks is not None and total_tracks > 0:

                    dates = [
                        datetime.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%SZ")
                        for track in response["tracks"]["items"]
                    ]

                    latest_date = max(dates)

                    if latest_date > last_updated:
                        details = extract_contacts(response["description"])
                        details["user"] = {"id": self.user, "name": self.username}
                        details["related_playlists"] = {(self.playlist_id, response["name"])}
                        data_queues["results"].add_contact(details)

        self.processed += 1
