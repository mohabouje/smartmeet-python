from smartmeet.core.profiler import profile
from abc import ABC, abstractmethod


class Element(ABC):
    """
    For the application programmer, elements are best visualized as black boxes. On the one end, you might put
    something in, the element does something with it and something else comes out at the other side.

    There are two different types of elements:

    * Source Elements: Source elements generate data for use by a pipeline. Source elements do not accept data,
     they only generate data.

    * Filter Elements: Filters and filter-like elements have both input and outputs pads. They operate on data that
    they receive on their input (sink) pads, and will provide data on their output (io) pads.

    By linking a io element with zero or more filter-like elements and finally a sink element, you set up a media
    pipeline. Data will flow through the elements. This is the basic concept of media handling.

    """
    def __init__(self, name: str = ""):
        """ Creates an Element with the given alias

        :param name: Element's name also known as alias
        """
        self.__sinks = []
        self.__name = name

    @profile
    def __run_processing(self, data, extra=None):
        return self.process(data, extra)

    def __propagate(self, data, extra=None):
        for sink in self.__sinks:
            sink.run(data, extra)

    @property
    def name(self) -> str:
        """ Returns the name (also known as alias) of the Element """
        return self.__name

    @abstractmethod
    def process(self, data, extra=None):
        """ Process the data

        This function process the data and returns the updated version. This function does not propagates the
        processing over the pipeline.

        :param data: Input data, generally a numpy array storing audio samples
        :param extra: Dictionary with any extra information
        :return: The processed data and any extra useful information
        """
        return data, extra

    def reset(self):
        """ Resets the Element to the original state, invalidating any previous computation. """
        pass

    def link(self, sink):
        """ Links the given Element

        This function is only applicable for producer-like elements. When an external element is linked, It will be
        part of the pipeline. The element may be called finishing the processing of the current element.

        :param sink: Element to be linked
        """
        if not issubclass(sink, Element):
            raise TypeError()
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
