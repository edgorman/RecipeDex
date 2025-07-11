from abc import ABC, abstractmethod


class RecipeStorage(ABC):

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def create(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def delete(self):
        ...
