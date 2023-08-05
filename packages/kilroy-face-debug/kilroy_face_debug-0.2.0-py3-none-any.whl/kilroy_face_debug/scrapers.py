from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncIterable, Optional, List, Dict, Any
from uuid import uuid4

from kilroy_face_server_py_sdk import (
    Categorizable,
    classproperty,
    normalize,
    SerializableState,
)
from kilroy_server_py_utils import Configurable, Parameter

from kilroy_face_debug.post import Post, PostTextData, PostData


class Scraper(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Scraper"))

    @abstractmethod
    def scrap(
        self,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> AsyncIterable[Post]:
        pass


# Dummy


class DummyScraperState(SerializableState):
    posts: List[str] = []


class DummyScraper(Scraper, Configurable[DummyScraperState]):
    class PostsParameter(Parameter[DummyScraperState, List[str]]):
        # noinspection PyMethodParameters
        @classproperty
        def schema(cls) -> Dict[str, Any]:
            return {
                "type": "array",
                "items": {"type": "string"},
                "title": cls.pretty_name,
                "default": [],
            }

    async def scrap(
        self,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> AsyncIterable[Post]:
        async with self.state.read_lock() as state:
            for post in state.posts:
                yield Post(
                    data=PostData(text=PostTextData(content=post)), id=uuid4()
                )
