from abc import ABC, abstractmethod


class ITelemetryService(ABC):

    @abstractmethod
    def library_loaded(self) -> None:
        pass
