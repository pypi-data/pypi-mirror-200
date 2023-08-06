from abc import ABCMeta, abstractmethod


class Consumer(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'consume') and
                callable(subclass.consume) and
                NotImplemented)

    @abstractmethod
    def consume(self, data: str):
        raise NotImplementedError
