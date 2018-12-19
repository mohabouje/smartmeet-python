from smartmeet.core.filter import Filter
from smartmeet.utils.converter import Converter
from webrtc_audio_processing import AudioProcessingModule as AP

class NoiseSuppressor(Filter):

    def __init__(self, rate: int, channels: int, level : int = 0, name: str = ""):
        """
        Creates a noise suppression element with the given configuration
        Args:
            rate (int): The audio sample rate, in Hz.
            channels (int): Number of channels
            level (int): Level of aggressiveness of the noise suppressor.
            name (str): Name of the element
        """
        super().__init__(name=name)
        self.__channels = channels
        self.__rate = rate
        self.__frames_per_channel = int(rate * 0.01)
        self.__ap = AP(enable_ns=True)
        self.__ap.set_ns_level(level)
        self.__ap.set_stream_format(rate, channels)

    @property
    def sample_rate(self) -> int:
        """ Returns the sampling rate in Hz """
        return self.__rate

    @property
    def channels(self) -> int:
        """ Returns the number of channels """
        return self.__channels

    @property
    def level(self) -> int:
        """ Returns the level of aggressiveness of the noise suppression element"""
        return self.__ap.ns_level()

    @level.setter
    def level(self, level: int):
        """
        Set the aggressiveness of the noise suppression element

        Args:
             level (int): Level of aggressiveness of the noise suppression element.
        """
        self.__ap.set_ns_level(level)

    def process(self, data, extra) -> tuple:
        """
        Checks if the given data contains human speech.
        Args:
            data: An array containing the data
            extra: Dictionary storing any extra information previously computed.

        Returns:
            A tuple with the filtered data
        """

        if data.shape() != [self.channels, self.__frames_per_channel]:
            raise ValueError("Invalid shape. Expected (%d, %d)" % (self.channels, self.__frames_per_channel))

        fixed = Converter.fromFloat16ToS16(data)
        fixed = Converter.interleave(fixed)
        fixed = self.__ap.process_stream(fixed)
        floating = Converter.deinterleave(fixed, frames_per_buffer=self.__frames_per_channel, channels=self.channels)
        floating = Converter.fromS16ToFloat16(floating)
        return floating, extra