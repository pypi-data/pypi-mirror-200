import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, AsyncIterable, Dict, Optional, Set, Tuple, Type
from uuid import UUID

from aiostream import stream
from aiostream.aiter_utils import aiter, anext

from kilroy_face_debug.post import Post
from kilroy_face_debug.posters import Poster, BasicPoster
from kilroy_face_debug.processors import Processor
from kilroy_face_debug.restrictions import Restriction
from kilroy_face_debug.scoring.modifiers import ScoreModifier
from kilroy_face_debug.scoring.raw import Scorer, RandomScorer
from kilroy_face_debug.scrapers import Scraper, DummyScraper
from kilroy_face_server_py_sdk import (
    Categorizable,
    CategorizableBasedParameter,
    Face,
    JSONSchema,
    Metadata,
    Parameter,
    Savable,
    SerializableModel,
    classproperty,
    normalize,
)
from kilroy_server_py_utils import (
    CategorizableBasedOptionalParameter,
    Configurable,
)

logger = logging.getLogger(__name__)


class Params(SerializableModel):
    poster_type: str = "basic"
    posters_params: Dict[str, Dict[str, Any]] = {}
    scorer_type: str = "random"
    scorers_params: Dict[str, Dict[str, Any]] = {}
    score_modifier_type: Optional[str] = None
    score_modifiers_params: Dict[str, Dict[str, Any]] = {}
    scraper_type: str = "dummy"
    scrapers_params: Dict[str, Dict[str, Any]] = {}
    restriction_type: Optional[str] = None
    restrictions_params: Dict[str, Dict[str, Any]] = {}


@dataclass
class State:
    processor: Processor
    poster: Poster
    posters_params: Dict[str, Dict[str, Any]]
    scorer: Scorer
    scorers_params: Dict[str, Dict[str, Any]]
    score_modifier: Optional[ScoreModifier]
    score_modifiers_params: Dict[str, Dict[str, Any]]
    scraper: Scraper
    scrapers_params: Dict[str, Dict[str, Any]]
    restriction: Optional[Restriction]
    restrictions_params: Dict[str, Dict[str, Any]]
    cache: Dict[UUID, Post]


class PosterParameter(CategorizableBasedParameter[State, Poster]):
    @classmethod
    async def _get_params(cls, state: State, category: str) -> Dict[str, Any]:
        return {**state.posters_params.get(category, {})}

    # noinspection PyMethodParameters
    @classproperty
    def default_categorizable(cls) -> Type[Poster]:
        return BasicPoster


class ScorerParameter(CategorizableBasedParameter[State, Scorer]):
    @classmethod
    async def _get_params(cls, state: State, category: str) -> Dict[str, Any]:
        return {**state.scorers_params.get(category, {})}

    # noinspection PyMethodParameters
    @classproperty
    def default_categorizable(cls) -> Type[Scorer]:
        return RandomScorer


class ScoreModifierParameter(
    CategorizableBasedOptionalParameter[State, ScoreModifier]
):
    @classmethod
    async def _get_params(cls, state: State, category: str) -> Dict[str, Any]:
        return {**state.score_modifiers_params.get(category, {})}


class ScraperParameter(CategorizableBasedParameter[State, Scraper]):
    @classmethod
    async def _get_params(cls, state: State, category: str) -> Dict[str, Any]:
        return {**state.scrapers_params.get(category, {})}

    # noinspection PyMethodParameters
    @classproperty
    def default_categorizable(cls) -> Type[Scraper]:
        return DummyScraper


class RestrictionParameter(
    CategorizableBasedOptionalParameter[State, Restriction]
):
    @classmethod
    async def _get_params(cls, state: State, category: str) -> Dict[str, Any]:
        return {**state.restrictions_params.get(category, {})}


class DebugFaceBase(Face[State], ABC):
    # noinspection PyMethodParameters
    @classproperty
    @abstractmethod
    def post_type(cls) -> str:
        pass

    @classmethod
    async def _build_processor(cls) -> Processor:
        return await cls._build_generic(Processor, category=cls.post_type)

    @classmethod
    async def _build_poster(cls, params: Params) -> Poster:
        return await cls._build_generic(
            Poster,
            category=params.poster_type,
            **params.posters_params.get(params.poster_type, {}),
        )

    @classmethod
    async def _build_scorer(cls, params: Params) -> Scorer:
        return await cls._build_generic(
            Scorer,
            category=params.scorer_type,
            **params.scorers_params.get(params.scorer_type, {}),
        )

    @classmethod
    async def _build_score_modifier(
        cls, params: Params
    ) -> Optional[ScoreModifier]:
        if params.score_modifier_type is None:
            return None
        return await cls._build_generic(
            ScoreModifier,
            category=params.score_modifier_type,
            **params.score_modifiers_params.get(
                params.score_modifier_type, {}
            ),
        )

    @classmethod
    async def _build_scraper(cls, params: Params) -> Scraper:
        return await cls._build_generic(
            Scraper,
            category=params.scraper_type,
            **params.scrapers_params.get(params.scraper_type, {}),
        )

    @classmethod
    async def _build_restriction(cls, params: Params) -> Optional[Restriction]:
        if params.restriction_type is None:
            return None
        return await cls._build_generic(
            Restriction,
            category=params.restriction_type,
            **params.restrictions_params.get(params.restriction_type, {}),
        )

    async def _build_default_state(self) -> State:
        params = Params(**self._kwargs)

        return State(
            processor=await self._build_processor(),
            poster=await self._build_poster(params),
            posters_params=params.posters_params,
            scorer=await self._build_scorer(params),
            scorers_params=params.scorers_params,
            score_modifier=await self._build_score_modifier(params),
            score_modifiers_params=params.score_modifiers_params,
            scraper=await self._build_scraper(params),
            scrapers_params=params.scrapers_params,
            restriction=await self._build_restriction(params),
            restrictions_params=params.restrictions_params,
            cache={},
        )

    @staticmethod
    async def _save_processor(state: State, directory: Path) -> None:
        if isinstance(state.processor, Savable):
            await state.processor.save(directory / "processor")

    @staticmethod
    async def _save_poster(state: State, directory: Path) -> None:
        if isinstance(state.poster, Savable):
            await state.poster.save(directory / "poster")

    @staticmethod
    async def _save_scorer(state: State, directory: Path) -> None:
        if isinstance(state.scorer, Savable):
            await state.scorer.save(directory / "scorer")

    @staticmethod
    async def _save_score_modifier(state: State, directory: Path) -> None:
        if isinstance(state.score_modifier, Savable):
            await state.score_modifier.save(directory / "score_modifier")

    @staticmethod
    async def _save_scraper(state: State, directory: Path) -> None:
        if isinstance(state.scraper, Savable):
            await state.scraper.save(directory / "scraper")

    @staticmethod
    async def _save_restriction(state: State, directory: Path) -> None:
        if isinstance(state.restriction, Savable):
            await state.restriction.save(directory / "restriction")

    @staticmethod
    async def _save_cache(state: State, directory: Path) -> None:
        serialized = {
            str(post_id): post.json() for post_id, post in state.cache.items()
        }
        with open(directory / "cache.json", "w") as f:
            json.dump(serialized, f)

    @staticmethod
    async def _create_state_dict(state: State) -> Dict[str, Any]:
        return {
            "processor_type": state.processor.category,
            "poster_type": state.poster.category,
            "scorer_type": state.scorer.category,
            "score_modifier_type": state.score_modifier.category
            if state.score_modifier is not None
            else None,
            "scraper_type": state.scraper.category,
            "restriction_type": state.restriction.category
            if state.restriction is not None
            else None,
            "posters_params": state.posters_params,
            "scorers_params": state.scorers_params,
            "score_modifiers_params": state.score_modifiers_params,
            "scrapers_params": state.scrapers_params,
            "restrictions_params": state.restrictions_params,
        }

    @classmethod
    async def _save_state(cls, state: State, directory: Path) -> None:
        await cls._save_processor(state, directory)
        await cls._save_poster(state, directory)
        await cls._save_scorer(state, directory)
        await cls._save_score_modifier(state, directory)
        await cls._save_scraper(state, directory)
        await cls._save_restriction(state, directory)
        await cls._save_cache(state, directory)
        state_dict = await cls._create_state_dict(state)
        await cls._save_state_dict(state_dict, directory)

    @classmethod
    async def _load_processor(
        cls, directory: Path, state_dict: Dict[str, Any]
    ) -> Processor:
        category = state_dict.get("processor_type", cls.post_type)
        return await cls._load_generic(
            directory / "processor",
            Processor,
            category=category,
            default=partial(cls._build_processor),
        )

    @classmethod
    async def _load_poster(
        cls, directory: Path, state_dict: Dict[str, Any], params: Params
    ) -> Poster:
        category = state_dict.get("poster_type", params.poster_type)
        return await cls._load_generic(
            directory / "poster",
            Poster,
            category=category,
            **state_dict.get("posters_params", params.posters_params).get(
                category, {}
            ),
            default=partial(cls._build_poster, params),
        )

    @classmethod
    async def _load_scorer(
        cls, directory: Path, state_dict: Dict[str, Any], params: Params
    ) -> Scorer:
        category = state_dict.get("scorer_type", params.scorer_type)
        return await cls._load_generic(
            directory / "scorer",
            Scorer,
            category=category,
            **state_dict.get("scorers_params", params.scorers_params).get(
                category, {}
            ),
            default=partial(cls._build_scorer, params),
        )

    @classmethod
    async def _load_score_modifier(
        cls, directory: Path, state_dict: Dict[str, Any], params: Params
    ) -> Optional[ScoreModifier]:
        if "score_modifier_type" in state_dict:
            category = state_dict["score_modifier_type"]
        else:
            category = params.score_modifier_type

        if category is None:
            return None
        return await cls._load_generic(
            directory / "score_modifier",
            ScoreModifier,
            category=category,
            **state_dict.get(
                "score_modifiers_params", params.score_modifiers_params
            ).get(category, {}),
            default=partial(cls._build_score_modifier, params),
        )

    @classmethod
    async def _load_scraper(
        cls, directory: Path, state_dict: Dict[str, Any], params: Params
    ) -> Scraper:
        category = state_dict.get("scraper_type", params.scraper_type)
        return await cls._load_generic(
            directory / "scraper",
            Scraper,
            category=category,
            **state_dict.get("scrapers_params", params.scrapers_params).get(
                category, {}
            ),
            default=partial(cls._build_scraper, params),
        )

    @classmethod
    async def _load_restriction(
        cls, directory: Path, state_dict: Dict[str, Any], params: Params
    ) -> Optional[Restriction]:
        if "restriction_type" in state_dict:
            category = state_dict["restriction_type"]
        else:
            category = params.restriction_type

        if category is None:
            return None
        return await cls._load_generic(
            directory / "restriction",
            Restriction,
            category=category,
            **state_dict.get(
                "restrictions_params", params.restrictions_params
            ).get(category, {}),
            default=partial(cls._build_restriction, params),
        )

    @staticmethod
    async def _load_cache(directory: Path) -> Dict[UUID, Post]:
        with open(directory / "cache.json", "r") as f:
            serialized = json.load(f)
        return {
            UUID(post_id): Post(**json.loads(post))
            for post_id, post in serialized.items()
        }

    async def _load_saved_state(self, directory: Path) -> State:
        state_dict = await self._load_state_dict(directory)
        params = Params(**self._kwargs)

        return State(
            processor=await self._load_processor(directory, state_dict),
            poster=await self._load_poster(directory, state_dict, params),
            posters_params=state_dict.get(
                "posters_params", params.posters_params
            ),
            scorer=await self._load_scorer(directory, state_dict, params),
            scorers_params=state_dict.get(
                "scorers_params", params.scorers_params
            ),
            score_modifier=await self._load_score_modifier(
                directory, state_dict, params
            ),
            score_modifiers_params=state_dict.get(
                "score_modifiers_params", params.score_modifiers_params
            ),
            scraper=await self._load_scraper(directory, state_dict, params),
            scrapers_params=state_dict.get(
                "scrapers_params", params.scrapers_params
            ),
            restriction=await self._load_restriction(
                directory, state_dict, params
            ),
            restrictions_params=state_dict.get(
                "restrictions_params", params.restrictions_params
            ),
            cache=await self._load_cache(directory),
        )

    async def cleanup(self) -> None:
        async with self.state.write_lock() as state:
            if isinstance(state.processor, Configurable):
                await state.processor.cleanup()
            if isinstance(state.poster, Configurable):
                await state.poster.cleanup()
            if isinstance(state.scorer, Configurable):
                await state.scorer.cleanup()
            if isinstance(state.score_modifier, Configurable):
                await state.score_modifier.cleanup()
            if isinstance(state.scraper, Configurable):
                await state.scraper.cleanup()
            if isinstance(state.restriction, Configurable):
                await state.restriction.cleanup()


class DebugFace(DebugFaceBase, Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("DebugFace"))

    # noinspection PyMethodParameters
    @classproperty
    def metadata(cls) -> Metadata:
        return Metadata(
            key="kilroy-face-debug", description="Kilroy face for debugging"
        )

    # noinspection PyMethodParameters
    @classproperty
    def post_type(cls) -> str:
        return cls.category

    # noinspection PyMethodParameters
    @classproperty
    def post_schema(cls) -> JSONSchema:
        return Processor.for_category(cls.post_type).post_schema

    # noinspection PyMethodParameters
    @classproperty
    def parameters(cls) -> Set[Type[Parameter]]:
        return {
            PosterParameter,
            ScorerParameter,
            ScoreModifierParameter,
            ScraperParameter,
            RestrictionParameter,
        }

    async def post(
        self, content: Dict[str, Any]
    ) -> Tuple[UUID, Optional[str]]:
        logger.info("Creating new post...")

        async with self.state.read_lock() as state:
            data = await state.processor.to_internal(content)
            if state.restriction is not None:
                if not await state.restriction.check(data):
                    raise ValueError("Post is not allowed to be posted.")
            post = await state.poster.post(state.cache, data)

        logger.info(f"New post id: {str(post.id)}.")
        return post.id, None

    async def score(self, id: UUID) -> float:
        logger.info(f"Scoring post {str(id)}...")

        async with self.state.read_lock() as state:
            post = state.cache[id]
            score = await state.scorer.score(post)
            if state.score_modifier is not None:
                score = await state.score_modifier.modify(post, score)

        logger.info(f"Score for post {str(id)}: {score}.")
        return score

    async def _fetch(
        self,
        posts: AsyncIterable[Post],
    ) -> AsyncIterable[Tuple[UUID, Dict[str, Any], float]]:
        posts = aiter(posts)

        while True:
            async with self.state.read_lock() as state:
                try:
                    post = await anext(posts)
                except StopAsyncIteration:
                    break

                score = await state.scorer.score(post)
                if state.score_modifier is not None:
                    score = await state.score_modifier.modify(post, score)

                try:
                    data = await state.processor.to_external(post.data)
                except Exception:
                    continue

                yield post.id, data, score

    async def scrap(
        self,
        limit: Optional[int] = None,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> AsyncIterable[Tuple[UUID, Dict[str, Any], float]]:
        async with self.state.read_lock() as state:
            posts = state.scraper.scrap(before, after)

        posts = self._fetch(posts)
        if limit is not None:
            posts = stream.take(posts, limit)
        else:
            posts = stream.iterate(posts)

        logger.info("Scraping posts...")

        async with posts.stream() as streamer:
            async for post_id, post, score in streamer:
                logger.info(f"Scraped post {str(post_id)}.")
                yield post_id, post, score

        logger.info("Scraping finished.")

    async def reset_self(self) -> None:
        logger.info("Resetting state...")
        await super().reset_self()
        logger.info("State reset.")

    async def save_self(self, directory: Path) -> None:
        logger.info("Saving state...")
        await super().save_self(directory)
        logger.info("State saved.")


class TextOnlyDebugFace(DebugFace):
    pass


class ImageOnlyDebugFace(DebugFace):
    pass


class TextAndImageDebugFace(DebugFace):
    pass


class TextOrImageDebugFace(DebugFace):
    pass


class TextWithOptionalImageDebugFace(DebugFace):
    pass


class ImageWithOptionalTextDebugFace(DebugFace):
    pass
