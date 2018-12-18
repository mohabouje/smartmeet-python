from smartmeet.core.element import Element
from smartmeet.core.sink import Sink
from smartmeet.core.profiler import profile
from abc import abstractmethod


class Source(Element):

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.__sinks = []

    @profile
    def __run_processing(self):
        return self.process()

    def __propagate(self, data, extra=None):
        for sink in self.__sinks:
            sink.run(data, extra)

    @abstractmethod
    def process(self):
        """ Generates a chunk of data

        This function generate a chunk of data

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        :return: The processed data and any extra useful information
        """
        pass

    def link(self, sink):
        """ Links the given Element

        This function is only applicable for producer-like elements. When an external element is linked, It will be
        part of the pipeline. The element may be called finishing the processing of the current element.

        :param sink: Element to be linked
        """
        if not issubclass(sink, Sink):
            raise TypeError()
        self.__sinks.append(sink)

    def unlink(self, sink):
        """ Un-links the given Element

        This function is only applicable for producer-like elements. When an external element is un-linked, It won't be
        called after processing the data. It won't be part of the current pipeline.

        :param sink: Element to be unlinked
        """
        self.__sinks.remove(sink)

    def run(self):
        """ Generate a chunk of data and send it to the different connected sinks.

        The function generate a chunk of data and propagates the results to all the different sinks that conform the
        pipeline.

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        data, extra = self.__run_processing()
        self.__propagate(data=data, extra=extra)