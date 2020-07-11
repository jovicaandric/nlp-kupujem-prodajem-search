from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Type, Any


PredictorType = TypeVar("PredictorType", bound="BasePredictor")
UserQueryProcessor = Callable[[str], str]


class BasePredictor(ABC):

    # mypy doesn't work with @abstractclassmethod
    @classmethod
    @abstractmethod
    def from_path(cls: Type[PredictorType], path: str) -> PredictorType:
        pass

    @abstractmethod
    def predict(self, user_query: str) -> Any:
        pass
