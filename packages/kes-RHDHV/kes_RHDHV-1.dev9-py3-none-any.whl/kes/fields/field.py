from abc import ABC, abstractmethod


class Field(ABC):
    @abstractmethod
    def is_empty(self) -> bool:
        pass
