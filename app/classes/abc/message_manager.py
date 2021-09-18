from abc import ABC, abstractmethod


class MessageManager(ABC):

    @abstractmethod
    def update(self):
        ...
