from abc import abstractmethod

from profilehooks import profile

from smartmeet.core.element import Element


class Sink(Element):
    """Sink elements are end points in a media pipeline. They accept data but do
    not produce anything. Disk writing, sound-card playback, and video output
    would all be implemented by sink elements.
    """

    def __init__(self, name: str = ""):
        """
        Args:
            name (str): Element's name also known as alias
        """
        super().__init__(name)
        self.__sinks = []

    @profile
    def __run_processing(self, data, extra):
        """
        Args:
            data:
            extra:
        """
        return self.process(data=data, extra=extra)

    @abstractmethod
    def process(self, data, extra):
        """Process a chunk of data

        Args:
            data: Input data, generally a numpy array storing audio samples
            extra: Dictionary with any extra information
        """

    def run(self, data, extra=None):
        """Runs the pipeline

        Args:
            data: Input data, generally a numpy array storing audio samples
            extra: Dictionary with any extra information
        """
        self.__run_processing(data=data, extra=extra)
