from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        """Converts the object to a dict of basic types."""
        pass
