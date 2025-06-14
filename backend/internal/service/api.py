from abc import ABC, abstractmethod


class APIService(ABC):

    @abstractmethod
    def run(self):
        ...
