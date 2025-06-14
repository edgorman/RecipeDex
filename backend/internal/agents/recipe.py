from abc import ABC, abstractmethod


class RecipeAgent(ABC):

    @abstractmethod
    def message(self):
        ...
