from abc import ABC, abstractmethod
from threading import Lock
from typing import Optional, Generic, TypeVar

from detoxify import Detoxify
from tweetnlp import Sentiment

ModelType = TypeVar("ModelType")


def fetch_models() -> None:
    ToxicityModelLoader.get()
    ToxicityModelLoader.release()
    SentimentModelLoader.get()
    SentimentModelLoader.release()


class ModelLoader(ABC, Generic[ModelType]):
    model: Optional[ModelType] = None
    reference_count: int = 0
    lock: Lock = Lock()

    @classmethod
    @abstractmethod
    def load(cls) -> ModelType:
        pass

    @classmethod
    def unload(cls) -> None:
        pass

    @classmethod
    def get(cls) -> ModelType:
        with cls.lock:
            if cls.model is None:
                cls.model = cls.load()
            cls.reference_count += 1
            return cls.model

    @classmethod
    def release(cls) -> None:
        with cls.lock:
            cls.reference_count -= 1
            if cls.reference_count == 0:
                cls.unload()
                cls.model = None


class ToxicityModelLoader(ModelLoader[Detoxify]):
    @classmethod
    def load(cls) -> Detoxify:
        return Detoxify("multilingual")


class SentimentModelLoader(ModelLoader[Sentiment]):
    @classmethod
    def load(cls) -> Sentiment:
        return Sentiment()
