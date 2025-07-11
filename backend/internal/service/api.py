from abc import ABC, abstractmethod


class APIService(ABC):
    """The APIService is the runnable service for API requests"""

    @abstractmethod
    def run(self):
        ...
