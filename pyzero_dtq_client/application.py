import abc


class Application(abc.ABC):

    @abc.abstractmethod
    def run(self, task):
        pass
