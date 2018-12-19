from smartmeet.core.element import Element
from smartmeet.core.source import Source


class Pipeline:
    """ This class performs pipelined execution

    A pipeline represents pipelined application of a series of Elements to a stream of raw data. A pipeline contains
    one or more filters, denoted here as $$ f_i $$, where $$ i $$ denotes the position of the filter in the pipeline.

    Note:
        If parallel processing is enabled, given sufficient processors and tokens, the throughput of the pipeline is
        limited to the throughput of the slowest serial filter.

    """

    def __init__(self, name: str = "default"):
        self.__name = name
        self.__elements = []

    def add(self, element: Element):
        """ Appends filter f to sequence of filters in the pipeline.
        Note:
            The filter f must not already be in a pipeline.
        :param element: Element to add to the pipeline
        """

        if not issubclass(type(element), Element):
            raise TypeError("Only Elements can be part of a pipeline")
        if not self.__elements and not issubclass(type(element), Source):
            raise TypeError(
                    "The first component of a pipeline must be a Source element"
            )
        if self.__elements and issubclass(type(element), Source):
            raise RuntimeError("A pipeline must have only one single source")
        if element in self.__elements:
            raise ValueError("The filter already exist in the pipeline")

        if self.__elements:
            self.__elements[-1].link(element)

        self.__elements.append(element)

    def run(self):
        """ Runs the pipeline until the end of the streaming and processing tasks.
        :return: A boolean representing if the pipeline has been executed successfully.
        """

        if not self.__elements:
            return False

        return Pipeline.exec(source=self.__elements[0])

    @staticmethod
    def exec(source: Source):
        """ Runs the pipeline until the source elements stop the streaming.
        The pipeline will stop when the source elements stop the streaming and each subsequent filter has processed
        all items from its predecessor.

        Note:
            A pipeline can be run multiple times. It is safe to add stages between runs.

        :param source: Source element which generate the raw data to be processed
        :return: A boolean representing if the pipeline has been executed successfully.
        """

        if not issubclass(type(source), Source):
            raise TypeError("Only Source objects can start a pipeline")

        source.start()
        while not source.done():
            try:
                source.run()
                print("Current timestamp: %s" % source.timestamp())
            except KeyboardInterrupt:
                source.stop()
                return False
        return True
