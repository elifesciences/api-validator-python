from abc import ABC, abstractmethod


class ResponseValidator(ABC):
    @abstractmethod
    def validate(self, response):
        raise NotImplementedError
