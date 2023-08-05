from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from random import random

from detoxify import Detoxify
from kilroy_face_server_py_sdk import Categorizable, classproperty, normalize
from kilroy_server_py_utils import Configurable, background
from tweetnlp import Sentiment

from kilroy_face_debug.models import ToxicityModelLoader, SentimentModelLoader
from kilroy_face_debug.post import Post


class Scorer(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Scorer"))

    @abstractmethod
    async def score(self, post: Post) -> float:
        pass


# Random


class RandomScorer(Scorer):
    async def score(self, post: Post) -> float:
        return random()


# Toxicity


@dataclass
class ToxicityScorerState:
    detoxify: Detoxify


class ToxicityScorer(Scorer, Configurable[ToxicityScorerState]):
    async def _build_default_state(self) -> ToxicityScorerState:
        return ToxicityScorerState(
            detoxify=await background(ToxicityModelLoader.get),
        )

    @classmethod
    async def _save_state(
        cls, state: ToxicityScorerState, directory: Path
    ) -> None:
        pass

    async def _load_saved_state(self, directory: Path) -> ToxicityScorerState:
        return await self._build_default_state()

    async def cleanup(self) -> None:
        await background(ToxicityModelLoader.release)

    async def score(self, post: Post) -> float:
        async with self.state.read_lock() as state:
            if not post.data.text:
                return 0.0
            return state.detoxify.predict(post.data.text.content)["toxicity"]


# Toxicity


@dataclass
class PositivityScorerState:
    model: Sentiment


class PositivityScorer(Scorer, Configurable[PositivityScorerState]):
    async def _build_default_state(self) -> PositivityScorerState:
        return PositivityScorerState(
            model=await background(SentimentModelLoader.get),
        )

    @classmethod
    async def _save_state(
        cls, state: PositivityScorerState, directory: Path
    ) -> None:
        pass

    async def _load_saved_state(
        self, directory: Path
    ) -> PositivityScorerState:
        return await self._build_default_state()

    async def cleanup(self) -> None:
        await background(SentimentModelLoader.release)

    async def score(self, post: Post) -> float:
        async with self.state.read_lock() as state:
            if not post.data.text:
                return 0.0
            pred = state.model.predict(
                post.data.text.content, return_probability=True
            )
            return pred["probability"]["positive"]
