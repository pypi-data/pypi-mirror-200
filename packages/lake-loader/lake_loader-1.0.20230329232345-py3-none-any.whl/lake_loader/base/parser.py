from abc import ABC, abstractmethod


# abstract base class
class BaseParser(ABC):
    @abstractmethod
    def parse_data(self, data):
        pass
