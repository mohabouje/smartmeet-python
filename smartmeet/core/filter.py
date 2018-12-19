from smartmeet.core.sink import Sink
from profilehooks import profile
from abc import abstractmethod


class Filter(Sink):

    def __init__(self, name: str = ""):
        """ Creates an Element with the given alias

        :param name: Element's name also known as alias
        """
        super().__init__(name)
        self.__sinks = []

    @profile
    def __run_processing(self, data, extra=None):
        return self.process(data, extra)

    def __propagate(self, data, extra=None):
        for sink in self.__sinks:
            sink.run(data, extra)

    @abstractmethod
    def process(self, data, extra):
        """ Process a chunk of data

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        pass

    def link(self, sink):
        """ Links the given Element

        This function is only applicable for producer-like elements. When an external element is linked, It will be
        part of the pipeline. The element may be called finishing the processing of the current element.

        :param sink: Element to be linked
        """
        if not issubclass(type(sink), Sink):
            raise TypeError("Only Sink objects can be linked")
        self.__sinks.append(sink)

    def unlink(self, sink):
        """ Un-links the given Element

        This function is only applicable for producer-like elements. When an external element is un-linked, It won't be
        called after processing the data. It won't be part of the current pipeline.

        :param sink: Element to be unlinked
        """
        self.__sinks.remove(sink)

    def run(self, data, extra=None):
        """ Runs the pipeline

        The function process the input data and propagates the results to all the different sinks that conform the
        pipeline.

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        data, extra = self.__run_processing(data, extra)
        self.__propagate(data, extra)