from .exceptions import QueueOverflowException
import time
import random


class BaseQueue:
    def __init__(self, limit=None, unique=False):
        self.limit = limit
        self.stack = []
        self.exhausted = []
        self.tail = -1
        self.last_updated = 0
        self.unique = unique

    def shuffle(self):
        random.shuffle(self.stack)

    def __str__(self) -> str:
        return f"Stack: {self.stack}"

    def get_timeout_stat(self, time, timeout):
        if self.last_updated == 0:
            return True
        return time - self.last_updated > timeout

    def has(self, item):
        return item in self.stack

    def addBack(self, item):
        if self.limit is not None and self.is_full():
            raise QueueOverflowException()

        if type(item) == list:
            add_item = item
            if len(item) + self.tail >= self.limit:
                print("Warning: Data to be added bigger than allowed. Truncating...")
                add_item = item[: self.limit - self.tail]
            self.stack.extend(add_item)
            self.tail += len(add_item)
        else:
            self.stack.append(item)
            self.tail += 1

    def addFront(self, item):
        if self.limit is not None and self.is_full():
            raise QueueOverflowException()

        if type(item) == list:
            add_item = item
            if len(item) + self.tail >= self.limit:
                print("Warning: Data to be added bigger than allowed. Truncating...")
                add_item = item[: self.limit - self.tail]
            self.stack = add_item + self.stack
            self.tail += len(add_item)
        else:
            self.stack.insert(0, item)
            self.tail += 1

    def removeBack(self):
        if self.tail == -1:
            return None
        item = self.stack[self.tail]
        self.stack.pop()
        self.tail -= 1
        return item

    def removeFront(self):
        if self.tail == -1:
            return None
        item = self.stack[0]
        self.stack.pop(0)
        self.tail -= 1
        return item

    def empty(self):
        self.stack = []
        self.tail = -1

    def is_empty(self):
        return self.tail == -1

    def is_full(self):
        return self.tail >= self.limit

    def get_size(self):
        return self.tail + 1

    def get_stack(self):
        return self.stack

    def add_exhausted(self, uid):
        self.exhausted.append(uid)

    def is_exhausted(self, uid):
        return uid in self.exhausted


class UserQueue(BaseQueue):
    def __init__(self):
        super().__init__(limit=20000)

    def has(self, item):
        if self.is_exhausted(item):
            return True
        return item in [x.uid for x in self.stack]


class ArtistQueue(BaseQueue):
    def __init__(self):
        super().__init__()

    def has(self, item):
        if self.is_exhausted(item):
            return True
        return item in self.stack


class ArtistPlaylistQueue(BaseQueue):
    def __init__(self):
        super().__init__()


class AlbumQueue(BaseQueue):
    def __init__(self):
        super().__init__()


class FollowerQueue(BaseQueue):
    def __init__(self):
        super().__init__(limit=40)


class SearchQueue(BaseQueue):
    def __init__(self):
        super().__init__()


class PlaylistQueue(BaseQueue):
    def __init__(self):
        super().__init__()


class PlaylistDetailedQueue(BaseQueue):
    def __init__(self):
        super().__init__()


class ResponseQueue(BaseQueue):
    def __init__(self, limit=100):
        super().__init__(limit=limit)

    def get_user(self, uid):
        for item in self.stack:
            if item.get("user") is not None and item.get("user") == uid:
                return item
        return None

    def is_full(self):
        user_count = 0
        for item in self.stack:
            link_count = (
                len(item["links"]["free"])
                + len(item["links"]["paid"])
                + len(item["email"])
            )
            if link_count > 0:
                user_count += 1

        return user_count >= self.limit

    def add_contact(self, contact):
        if self.is_full():
            raise QueueOverflowException()

        # Remove already existing items from contact

        for item in self.stack:
            for key in item:
                if key == "user":
                    continue
                if type(item[key]) == set:
                    # Removing duplicate items # for related plalists
                    contact[key] = {x for x in contact[key] if x not in item[key]}
                elif type(item[key]) == dict:
                    # Removing duplicate items
                    for subkey in item[key]:
                        contact[key][subkey] = {
                            x
                            for x in contact[key][subkey]
                            if x not in item[key][subkey]
                        }

        related_user = self.get_user(contact["user"]["id"])

        if related_user is not None:
            related_user["links"]["free"].update(contact["links"]["free"])
            related_user["links"]["paid"].update(contact["links"]["paid"])
            related_user["links"]["others"].update(contact["links"]["others"])
            related_user["email"].update(contact["email"])
            related_user["phone"].update(contact["phone"])
            related_user["related_playlists"].update(contact["related_playlists"])

            return True
        else:
            if (
                len(contact["links"]["free"]) > 0
                or len(contact["links"]["paid"]) > 0
                or len(contact["email"]) > 0
                or len(contact["phone"]) > 0
            ):
                self.addBack(contact)
                return True

        return False
