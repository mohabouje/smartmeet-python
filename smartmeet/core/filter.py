from abc import abstractmethod

from profilehooks import profile

from smartmeet.core.sink import Sink


class Filter(Sink):
    """Filters and filter-like elements have both input and outputs pads. hey
    operate on data that they receive on their input (sink) pads, and will
    provide data on their output (source) pads.
    """

    def __init__(self, name: str = ""):
        """Creates an Element with the given alias

        Args:
            name (str): Element's name also known as alias
        """
        super().__init__(name)
        self.__sinks = []

    @abstractmethod
    def process(self, data, extra) -> tuple:
        """Process a chunk of data

        Args:
            data: Input data, generally a numpy array storing audio samples
            extra: Dictionary with any extra information
        """

    def link(self, sink: Sink):
        """Links the given Element

        This function is only applicable for producer-like elements. When an
        external element is linked, It will be part of the pipeline. The element
        may be called with the results of the processing of the current element.

        Args:
            sink (Sink): Element to be linked
        """
        if not issubclass(type(sink), Sink):
            raise TypeError("Only Sink objects can be linked")
        self.__sinks.append(sink)

    def unlink(self, sink: Sink):
        """Un-links the given Element

        This function is only applicable for producer-like elements. When an
        external element is un-linked, It won't be called after processing the
        data. It won't be part of the current pipeline.

        Args:
            sink (Sink): Element to be unlinked
        """
        self.__sinks.remove(sink)

    def run(self, data, extra=None):
        """Runs the pipeline

        The function process the input data and propagates the results to all
        the different sinks that conform the pipeline.

        Args:
            data: Input data, generally a numpy array storing audio samples
            extra: Dictionary with any extra information
        """
        data, extra = self.__run_processing(data, extra)
        self.__propagate(data, extra)

    @profile
    def __run_processing(self, data, extra):
        """
        Args:
            data:
            extra:
        """
        return self.process(data, extra)

    def __propagate(self, data, extra):
        """
        Args:
            data:
            extra:
        """
        for sink in self.__sinks:
            sink.run(data, extra)
