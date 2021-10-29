import abc
from typing import List


class BaseModule(abc.ABC):

    @abc.abstractproperty
    def supported_message_types(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self, data: any):
        raise NotImplementedError()
