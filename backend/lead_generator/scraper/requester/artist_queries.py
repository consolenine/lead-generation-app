from .queries import BaseQuery, PersistedQuery, UserFromPlaylistQuery
from .exceptions import QueryFailedException


class ArtistDiscoveredOnQuery(BaseQuery, PersistedQuery):
    def __init__(self, artist):
        self.artist = artist

        super().__init__("https://api-partner.spotify.com/pathfinder/v1/query")

    async def process(
        self,
        session,
        headers,
        persisted_hash,
        callback_queues,
        data_queues,
        filters=None,
    ):
        data = f"?operationName=queryArtistDiscoveredOn&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A{self.artist}%22%7D&extensions={persisted_hash}"
        self.url += data

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Data for {self.artist} not found")
                    self.processed += 1
                    return
                print(self.url)
                if response == 400:
                    self.processed += 1
                    return
                raise QueryFailedException(
                    f"Failed to get albums: {response}", {"status": response}
                )
            self.processed += 1
            return

        try:
            items = (
                response.get("data")
                .get("artistUnion")
                .get("relatedContent")
                .get("discoveredOnV2")
                .get("items")
            )
        except Exception as e:
            self.processed += 1
            return

        if items is not None:
            for item in items:
                if item.get("data") is not None and item["data"].get("uri") is not None:
                    playlist_id = item["data"]["uri"].split(":")[-1]
                    owner_query = UserFromPlaylistQuery(playlist_id)
                    callback_queues["playlists"].addBack(owner_query)

        self.processed += 1


class ArtistFeaturingQuery(BaseQuery, PersistedQuery):
    def __init__(self, artist):
        self.artist = artist

        super().__init__("https://api-partner.spotify.com/pathfinder/v1/query")

    async def process(
        self,
        session,
        headers,
        persisted_hash,
        callback_queues,
        data_queues,
        filters=None,
    ):
        data = f"?operationName=queryArtistFeaturing&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A{self.artist}%22%7D&extensions={persisted_hash}"
        self.url += data

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Data for {self.artist} not found")
                    self.processed += 1
                    return
                if response == 400:
                    self.processed += 1
                    return
                print(self.url)
                raise QueryFailedException(
                    f"Failed to get albums: {response}", {"status": response}
                )
            self.processed += 1
            return

        try:
            items = (
                response.get("data")
                .get("artistUnion")
                .get("relatedContent")
                .get("featuringV2")
                .get("items")
            )
        except Exception as e:
            self.processed += 1
            return

        if items is not None:
            for item in items:
                if item.get("data") is not None and item["data"].get("uri") is not None:
                    playlist_id = item["data"]["uri"].split(":")[-1]
                    owner_query = UserFromPlaylistQuery(playlist_id)
                    callback_queues["playlists"].addBack(owner_query)

        self.processed += 1


class ArtistRelatedQuery(BaseQuery, PersistedQuery):
    def __init__(self, artist):
        self.artist = artist

        super().__init__("https://api-partner.spotify.com/pathfinder/v1/query")

    async def process(
        self,
        session,
        headers,
        persisted_hash,
        callback_queues,
        data_queues,
        filters=None,
    ):
        data = f"?operationName=queryArtistRelated&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A{self.artist}%22%7D&extensions={persisted_hash}"
        self.url += data

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Data for {self.artist} not found")
                    self.processed += 1
                    return
                if response == 400:
                    self.processed += 1
                    return
                print(self.url)
                raise QueryFailedException(
                    f"Failed to get albums: {response}", {"status": response}
                )
            self.processed += 1
            return

        try:
            items = (
                response.get("data")
                .get("artistUnion")
                .get("relatedContent")
                .get("relatedArtists")
                .get("items")
            )
        except Exception as e:
            self.processed += 1
            return

        if items is not None:
            for item in items:
                if item.get("id") is not None:
                    if not data_queues["artists"].has(item["id"]):
                        data_queues["artists"].addBack(item["id"])

        self.processed += 1


class ArtistAlbumsQuery(BaseQuery, PersistedQuery):
    def __init__(self, album_id):
        self.album_id = album_id

        super().__init__("https://api-partner.spotify.com/pathfinder/v1/query")

    async def process(
        self,
        session,
        headers,
        persisted_hash,
        callback_queues,
        data_queues,
        filters=None,
    ):
        data = f"?operationName=getAlbum&variables=%7B%22uri%22%3A%22spotify%3Aalbum%3A{self.album_id}%22%2C%22locale%22%3A%22%22%2C%22offset%22%3A0%2C%22limit%22%3A50%7D%7D&extensions={persisted_hash}"
        self.url += data

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Data for {self.album_id} not found")
                    self.processed += 1
                    return
                if response == 400:
                    self.processed += 1
                    return
                print(self.url)
                raise QueryFailedException(
                    f"Failed to get albums: {response}", {"status": response}
                )
            self.processed += 1
            return

        try:
            items = response.get("data").get("albumUnion").get("tracks").get("items")
        except Exception as e:
            self.processed += 1
            return

        if items is not None:
            for item in items:
                try:
                    artists = item["track"]["artists"]["items"]
                    for artist in artists:
                        artist_id = artist["uri"].split(":")[-1]
                        if not data_queues["artists"].has(artist_id):
                            data_queues["artists"].addBack(artist_id)
                except Exception as e:
                    continue

        self.processed += 1


class ArtistAppearsOnQuery(BaseQuery, PersistedQuery):
    def __init__(self, artist):
        self.artist = artist

        super().__init__("https://api-partner.spotify.com/pathfinder/v1/query")

    async def process(
        self,
        session,
        headers,
        persisted_hash,
        callback_queues,
        data_queues,
        filters=None,
    ):
        data = f"?operationName=queryArtistAppearsOn&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A{self.artist}%22%7D&extensions={persisted_hash}"
        self.url += data

        response = await self.getAsync(session, headers)
        if type(response) == int:
            if response >= 400 and response < 500:
                if response == 404:
                    print(f"Data for {self.artist} not found")
                    self.processed += 1
                    return
                if response == 400:
                    self.processed += 1
                    return
                print(self.url)
                raise QueryFailedException(
                    f"Failed to get albums: {response}", {"status": response}
                )
            self.processed += 1
            return

        try:
            items = (
                response.get("data")
                .get("artistUnion")
                .get("relatedContent")
                .get("appearsOn")
                .get("items")
            )
        except Exception as e:
            self.processed += 1
            return

        if items is not None:
            for item in items:
                try:
                    album_id = item.get("releases").get("items")[0].get("id")
                    callback_queues["albums"].addBack(album_id)
                except Exception as e:
                    continue

        self.processed += 1
