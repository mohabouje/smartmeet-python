from smartmeet.core.element import Element
from abc import abstractmethod
from smartmeet.core.profiler import profile


class Sink(Element):

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.__sinks = []

    @profile
    def __run_processing(self, data, extra=None):
        return self.process(data, extra)

    @abstractmethod
    def process(self, data, extra):
        """ Process a chunk of data

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        pass

    def run(self, data, extra):
        """ Runs the pipeline

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        self.__run_processing(data=data, extra=extra)
