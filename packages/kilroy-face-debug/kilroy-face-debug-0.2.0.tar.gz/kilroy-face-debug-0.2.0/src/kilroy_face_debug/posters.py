from abc import ABC, abstractmethod
from typing import MutableMapping
from uuid import UUID, uuid4

from kilroy_server_py_utils import Categorizable, classproperty, normalize

from kilroy_face_debug.post import PostData, Post


class Poster(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Poster"))

    @abstractmethod
    async def post(
        self, cache: MutableMapping[UUID, Post], data: PostData
    ) -> Post:
        pass


# Basic


class BasicPoster(Poster):
    async def post(
        self, cache: MutableMapping[UUID, Post], data: PostData
    ) -> Post:
        uid = uuid4()
        post = Post(data=data, id=uid)
        cache[uid] = post
        return post
