from abc import abstractmethod

from profilehooks import profile

from smartmeet.core.element import Element
from smartmeet.core.sink import Sink


class Source(Element):
    """
    A source element holds an streaming that generates raw data for use by a pipeline, for example reading from disk
    or from a sound card. Those components do not have a sink pad, so source elements do not accept data, they only
    generate data.
    """

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.__sinks = []

    @abstractmethod
    def process(self):
        """ Generates a chunk of data

        This function generate a chunk of data

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        :return: The processed data and any extra useful information
        """

    @abstractmethod
    def done(self):
        """ Checks if the source is generating data """

    @abstractmethod
    def start(self):
        """ Starts the streaming """

    @abstractmethod
    def stop(self):
        """ Stops the streaming """

    @abstractmethod
    def timestamp(self):
        """ Return the streaming timestamp """

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

    def run(self):
        """ Generate a chunk of data and send it to the different connected sinks.

        The function generate a chunk of data and propagates the results to all the different sinks that conform the
        pipeline.

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        """
        data, extra = self.__run_processing()
        self.__propagate(data=data, extra=extra)

    @profile
    def __run_processing(self):
        return self.process()

    def __propagate(self, data, extra):
        for sink in self.__sinks:
            sink.run(data, extra)
