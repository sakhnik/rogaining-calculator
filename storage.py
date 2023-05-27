from abc import ABC, abstractmethod
from position import Position


class Storage(ABC):
    @abstractmethod
    def get_start_position(self) -> Position:
        pass

    @abstractmethod
    def get_finish_position(self) -> Position:
        pass

    @abstractmethod
    def get_control_position(self, code: int) -> Position:
        pass

    @abstractmethod
    def get_name(self, number: int) -> str:
        pass

    @abstractmethod
    def get_class(self, number: int) -> str:
        pass


class DummyStorage(Storage):
    def get_start_position(self) -> Position:
        return Position()

    def get_finish_position(self) -> Position:
        return Position()

    def get_control_position(self, code: int) -> Position:
        return Position()

    def get_name(self, number: int) -> str:
        return "Foo Bar"

    def get_class(self, number: int) -> str:
        return "Open"
