from abc import ABC, abstractmethod
from position import Position


class Storage(ABC):
    @abstractmethod
    def get_start_position() -> Position:
        pass

    @abstractmethod
    def get_finish_position() -> Position:
        pass

    @abstractmethod
    def get_control_position(code: int) -> Position:
        pass
