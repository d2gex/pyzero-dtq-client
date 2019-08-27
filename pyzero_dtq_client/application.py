import abc


class Application(abc.ABC):

    @abc.abstractmethod
    def get_task(self):
        pass

    @abc.abstractmethod
    def add_result(self, result):
        pass

    @abc.abstractmethod
    def get_results(self):
        pass

    @abc.abstractmethod
    def done(self):
        pass
